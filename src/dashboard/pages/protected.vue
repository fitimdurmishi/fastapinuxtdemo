<template>
    <div>
      <h1>Protected Page</h1>
      <button @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    middleware: 'auth',
    methods: {
      logout() {
        this.$auth.logout();
        this.$router.push('/login');
      },
    },
  };
</script>
