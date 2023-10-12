<template>
  <div>
    <b-navbar toggleable="sm" type="dark" variant="info" sticky>
      <!-- <b-navbar-brand href="/">Home</b-navbar-brand> -->
  
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
  
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav v-if="isAuthenticated">
          <NuxtLink to="/authors" class="navbar-link">Authors</NuxtLink>
        </b-navbar-nav>
        <b-navbar-nav v-if="isAuthenticated" class="pl-3">
          <NuxtLink to="/books" class="navbar-link">Books</NuxtLink>
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
        this.$auth.logout(); // logout using the 'auth' middleware
        this.$router.push('/login'); // redirect to login page
      },
      login() {
        this.$router.push("/login");
      },
    },
}
</script>

<style>
.navbar-link {
  color: white !important;
}
</style>