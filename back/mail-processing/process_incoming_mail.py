import os
import uuid
from datetime import datetime

import boto3
import mailparser

from utils.mail_sender import send_mail_to_user
from utils.models import IdeaModel, UserModel

AWS_REGION = os.environ['SES_AWS_REGION']
SES_S3_BUCKET_NAME = os.environ['SES_S3_BUCKET_NAME']
MAILBOX_ADDR = os.environ['MAILBOX_ADDR']
BASE_SITE_URL = f"https://{os.environ['DOMAIN_NAME']}/"

s3 = boto3.client('s3')
ses = boto3.client('ses', region_name=AWS_REGION)

def get_confirm_mail_text(idea):
    return f"""
Great work! Just letting you know we got your idea!
Here's a link for you to view it online: {BASE_SITE_URL}ideas/{idea.ideaId}
You can always add on to it or edit it later by logging in.
---------------------
Title: {idea.title}
Detail:
{idea.content}
---------------------
View all your previous ideas [here](login link).

"""


def processIncomingMail(parsed_email):
    from_email = parsed_email.from_
    found_users = UserModel.emailIndex.query(from_email[0][1])
    user = None
    for found_user in found_users:
        user = found_user
    if not user:
        # TOdo process email from user that dont registered
        return

    idea = IdeaModel(str(uuid.uuid4()), user.userId)
    content_parsed =  (parsed_email.text_plain and parsed_email.text_plain[0]) or \
                   (parsed_email.text_html and parsed_email.text_html[0])
    content_lines = []
    for line in content_parsed.splitlines()[1:]:
        if MAILBOX_ADDR in line:
            break
        content_lines.append(line)
    idea.content = "\n".join(content_lines)
    idea.title = content_parsed.splitlines()[0]
    idea.createdDate = datetime.now()
    idea_date_str = parsed_email.subject.split('[Daily Idea] Idea for ', 1)[1]
    idea.ideaDate = datetime.strptime(idea_date_str, '%a %b %d %Y')
    idea.save()
    return idea


def endpoint(event, context):
    if 'ses' not in event['Records'][0]:
        print('this was not an SES event.  event["Records"][0]["ses"] not found')
        return
    ses_notification = event['Records'][0]['ses']
    mail_message_id = ses_notification['mail']['messageId']
    print(f"Message Id received: {mail_message_id}")

    try:
        data = s3.get_object(Bucket=SES_S3_BUCKET_NAME, Key=mail_message_id)
        raw_email = data['Body'].read()
        parsed_email = mailparser.parse_from_string(raw_email.decode('utf-8'))
        idea = processIncomingMail(parsed_email)
        send_mail_to_user(parsed_email.from_[0][1], f"Re: {parsed_email.subject}", get_confirm_mail_text(idea), None)
    except Exception as e:
        print(e)
        raise e
