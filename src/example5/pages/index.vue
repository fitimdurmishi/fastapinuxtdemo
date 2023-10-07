<template>
  <div>
    <h2>Hello</h2>
    <ul v-for="a in authors" v-bind:key="a.id">
      <li>{{a.name}}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data: () => ({
		authors: [],
	}),
  mounted() {
    this.getAuthors()
  },
  methods: {
    async getAuthors() {
      // let res = this.$store.dispatch("/authors/");
      let res = await this.$axios.get('/authors');
      this.authors = res.data;
      console.log(this.authors);
    },
  },
}
</script>
