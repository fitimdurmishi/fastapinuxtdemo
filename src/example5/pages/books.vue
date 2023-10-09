<template>
    <div>
        <ul v-for="b in books" v-bind:key="b.id">
            <li>Title: {{b.name}}, {{b.page_numbers}} pages from author {{b.author_id}}</li>
        </ul>
    </div>
</template>

<script>
    export default {
      layout: 'navigation',
      name: 'BooksPage',
      data: () => ({
              books: [],
          }),
      mounted() {
          this.getBooks()
      },
      methods: {
          async getBooks() {
          let res = await this.$axios.get('http://127.0.0.1:8000/books');
          this.books = res.data;
          console.log(this.books);
          },
      },
    }
</script>