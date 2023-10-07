<template>
    <div>
      <h1>Data from API</h1>
      <ul>
        <li v-for="item in apiData" :key="item.id">{{ item.title }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
        return {
        apiData: [],
        };
    },
    async asyncData() {
      try {
        const response = await this.$axios.get('/posts');
        return { apiData: response.data };
      } catch (error) {
        console.error('Error fetching data:', error);
        return { data: [] };
      }
    }
  };
  </script>
  