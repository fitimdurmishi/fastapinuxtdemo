<template>
    <div>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" placeholder="Password" type="password" />
      <button @click="login">Login</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: '',
      };
    },
    methods: {
      async login() {
        try {
          await this.$auth.loginWith('local', {
            data: {
                id: 0,
              username: this.username,
              password: this.password,
            },
          });

          // Access the user data from the response
        // const userData = response.data.user;
        const userData = this.username;
        

        // Handle user data as needed

          // Redirect to a protected page after successful login
          this.$router.push('/protected');
        } catch (error) {
          console.error('Login failed:', error);
        }
      },
    },
  };
  </script>
  