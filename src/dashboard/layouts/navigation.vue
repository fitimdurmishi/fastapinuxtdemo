<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info" >
      <b-navbar-brand href="/">Home</b-navbar-brand>
  
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="isAuthenticated">
          <b-nav-item href="/authors">Authors</b-nav-item>
          <b-nav-item href="/authors">Books</b-nav-item>
        </b-navbar-nav>
  
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">


          <!-- <b-button size="sm" @click="logout">Logout</b-button> -->

          <li v-if="isAuthenticated">
            <!-- {{ loggedInUser.username }} -->
            <b-button size="sm" @click="logout">Logout</b-button>
          </li>
          <li v-else>
            <b-button size="sm" @click="login">Login</b-button>
          </li>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    
    <Nuxt />
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    computed: {
      ...mapGetters(['isAuthenticated', 'loggedInUser'])
    },
    methods: {
      logout() {
        this.$auth.logout();
        this.$router.push('/login');
      },
      login() {
        this.$router.push("/login");
      },
    },
}
</script>
