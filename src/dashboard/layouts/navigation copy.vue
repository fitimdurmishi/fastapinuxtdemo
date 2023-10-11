<template>
    <div>
        <div class="pt-5">
            <nav>
                <ul>
                  <li>
                    <NuxtLink to="/">Home</NuxtLink>
                  </li>
                  <li>
                    <NuxtLink to="/authors">Authors</NuxtLink>
                  </li>
                  <li>
                    <NuxtLink to="/books">Books</NuxtLink>
                  </li>
                  <div>
                    <li v-if="isAuthenticated" class="float-right">
                      <!-- {{ loggedInUser.username }} -->
                      <!-- <NuxtLink to="/logout">Log Out</NuxtLink> -->
                      <b-button variant="light" @click="logout">Logout</b-button>
                      <NuxtLink to="/protected">Protected</NuxtLink>
                    </li>
                    <li v-else>
                      <NuxtLink to="/login">Log In</NuxtLink>
                      <NuxtLink to="/protected">Protected</NuxtLink>
                    </li>
                  </div>                  
                </ul>
            </nav>
        </div>
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
    },
}

</script>

<style>
/* home route and active route will show in bold as it matches / and /about */
a.nuxt-link-active {
  font-weight: bold;
}
/* exact link will show the primary color for only the exact matching link */
a.nuxt-link-exact-active {
  color: #00c58e;
}

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto,
    Helvetica Neue, Arial, Noto Sans, sans-serif, Apple Color Emoji,
    Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
  margin: 0;
}

main {
  margin: 0 auto;
  padding: 0 1rem;
  margin-top: 100px;
  max-width: 1280px;
  text-align: center;
}
img {
  margin-bottom: 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
li {
  margin: 0 0.5rem;
  padding: 0.25rem;
  font-size: 1.2rem;
}

nav {
  padding: 0 1rem;
}

a,
a:visited {
  text-decoration: none;
  color: inherit;
}

a:hover {
  color: #00c58e;
}

</style>