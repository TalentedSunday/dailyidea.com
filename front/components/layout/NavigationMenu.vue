<template>
  <v-navigation-drawer
    v-model="showSideMenu"
    class="sidebarMenu"
    absolute
    temporary
  >

    <v-list dense dark>
     <div class="logo-container">
        <img
          src="~/assets/images/bulb_white_on.png"
          class="logo-container__image"
        />
        <span class="logo-container__text">D A I L Y I D E A</span>
        <v-icon class="logo-container__icon" @click.native="close"
          >fa-times</v-icon
        >
      </div>
      <v-list-item
        active-class="highlighted"
        :class="'/ideas/all' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/ideas/all')"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-lightbulb-on</v-icon>All Ideas</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        active-class="highlighted"
        :class="'/ideas/me' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/ideas/me')"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-head-lightbulb</v-icon>My
            Ideas</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        active-class="highlighted"
        :class="'/ideas/liked' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/ideas/liked')"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-bookmark</v-icon>Favorite Ideas</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        active-class="highlighted"
        :class="'/profile' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/profile')"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-account-circle</v-icon>My
            Profile</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="isAuthenticated"
        active-class="highlighted"
        :class="'/settings' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/settings')"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-cog</v-icon>Settings</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
       <v-list-item
        v-if="isAuthenticated"
      >
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-account-circle</v-icon>FAQ</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="isAuthenticated" @click.native="signOut">
        <v-list-item-content>
          <v-list-item-title
            ><v-icon small>mdi-exit-run</v-icon>Sign Out</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="!isAuthenticated"
        active-class="highlighted"
        :class="'/auth/login' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/auth/login')"
      >
        <v-list-item-content>
          <v-list-item-title>Log In</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item
        v-if="!isAuthenticated"
        active-class="highlighted"
        :class="'/auth/signup' === $route.path ? 'highlighted' : ''"
        @click.native="openPage('/auth/signup')"
      >
        <v-list-item-content>
          <v-list-item-title>Sign Up</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'SiteNavigation',
  data() {
    return {
      showSideMenu: false
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.userData.isAuthenticated
    }
  },
  methods: {
    close() {
      this.showSideMenu = false
    },
    openPage(to) {
      this.showSideMenu = false
      this.$router.push(to)
    },
    signOut() {
      this.showSideMenu = false
      this.$emit('signOut')
    },
    show() {
      this.showSideMenu = true
    }
  }
}
</script>

<style scoped lang="scss">
.sidebarMenu {
  background: $primary-color !important;
  z-index: 999;
  .logo-container {
    margin-top: 3vh;
    margin-bottom: 4vh;
    padding-left: 16px;
    /*text-align: center;*/

    &__image {
      height: 20px;
      vertical-align: top;
      margin-right: 3px;
    }

    &__text {
      vertical-align: top;
      line-height: 22px;
      font-size: 14px;
    }

    &__icon {
      margin-right: 70px;
      float: left;
      display: inline-block;
      font-size: 21px;
      vertical-align: top;
      cursor: pointer;
    }
  }

 .logo-container,.logo-container .v-icon{
      color:white;
      font-size:12px;
    }
    .logo-container .v-icon{
      padding-right:5px;
      margin-left:10px;
    
    }
    .logo-container  .logo-container__icon{
      float:left;
      padding-top:3px;
    }
  // display: none;
  .v-list-item {
    cursor: pointer;
    i.v-icon {
      vertical-align: baseline;
      margin-right: 0.5rem;
    }
    &:hover,
    &:active {
      background-color: rgba(0, 0, 0, 0.2);
      .v-list-item__title {
        padding-left: 8px;
      }
    }
   
    .v-list-item__content {
      margin: 10px 0 !important;
      .nuxt-link-exact-active.nuxt-link-active {
        text-decoration: none;
      }
      .v-list-item__title {
        font-size: 16px;
        line-height: normal !important;
        color: white;
        i.v-icon {
          color: white;
        }
      }
    }
  }
}
.highlighted {
  border-left: 4px solid $secondary-color;
  .v-list-item__title,
  .v-list-item__title i.v-icon {
    color: $secondary-color !important;
  }
}
</style>