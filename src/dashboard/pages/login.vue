<template>
    <div id="outPopUp">
      <b-row >
        <!-- <input v-model="username" placeholder="Username" /> -->
        <b-form-input v-model="username" placeholder="Enter the username"></b-form-input>
      </b-row>
      <b-row class="pt-2">
        <!-- <input v-model="password" placeholder="Password" type="password" /> -->
        <b-form-input v-model="password" type="password" placeholder="Enter the password"></b-form-input>
      </b-row>
      <b-row class="pt-2">
        <b-button @click="login" class="text-center">Login</b-button>
      </b-row>      
    </div>
</template>
  
  <script>
  export default {
    data() {
      return {
        username: 'fito',
        password: 'fito',
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

         
          // this.$store.dispatch('auth/storeLoggedUser', this.username);
        

          // Handle user data as needed

          // Redirect to a protected page after successful login
          this.$router.push('/authors');
        } catch (error) {
          console.error('Login failed:', error);
        }
      },
    },
  };
  </script>

<style>
#outPopUp {
  position: absolute;
  width: 300px;
  height: 200px;
  z-index: 15;
  top: 50%;
  left: 50%;
  margin: -100px 0 0 -150px;
  background: rgb(255, 255, 255);
}
</style>
  