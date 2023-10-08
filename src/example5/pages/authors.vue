<template>
    <b-container fluid class="p-5">
        <b-row>
            <b-col lg="6" class="mb-2">
                <b-form-group
                  label="Filter"
                  label-for="filter-input"
                  label-cols-sm="3"
                  label-align-sm="right"
                  label-size="sm"
                  class="mb-0"
                >
                  <b-input-group size="sm">
                    <b-form-input
                      id="filter-input"
                      v-model="filter"
                      type="search"
                      placeholder="Type to Search"
                    ></b-form-input>
        
                    <b-input-group-append>
                      <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                    </b-input-group-append>
                  </b-input-group>
                </b-form-group>
            </b-col>
            <b-col lg="6" class="mb-2 text-right">
                <b-button size="sm" v-on:click="createAuthor">Create Author</b-button>
            </b-col>
        </b-row>

        <b-table 
            small 
            hover 
            :items="authorsWithBooks" 
            :fields="fields"
            :filter="filter"
            :filter-included-fields="filterOn"
            @row-clicked="myRowClickHandler"
        >
            <template #cell(actions)="row">
                <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">
                    Info modal
                </b-button>
                </template>
        </b-table>

        

        <!-- Info modal -->
        <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
            <pre>{{ infoModal.content }}</pre>
        </b-modal>
    </b-container>
</template>

<script>
    export default {
        layout: 'navigation',
        name: 'AuthorsPage',
        data: () => ({
            authorsWithBooks: [],
            fields: [{
                    key: "id",
                    label: "Id"
                },
                {
                    key: "name",
                    label: "Name"
                },
                {
                    key: "books.length",
                    label: "Nr. of books"
                }
            ],
            infoModal: {
                id: 'info-modal',
                title: '',
                content: ''
            },
            filter: null,
            filterOn: [],
        }),
        async mounted() {
            await this.loadDataFromDB();
        },
        methods: {
            async loadDataFromDB() {
                let resAuthors = await this.$axios.get('/authors');
                let allAuthors = resAuthors.data;
                let resBooks = await this.$axios.get('/books/');
                let allBooks = resBooks.data;

                this.authorsWithBooks = [];
                for (let i = 0; i < allAuthors.length; i++) {
                    let author = allAuthors[i];
                    let filteredBookByAuthor = allBooks.filter(b => b.author_id == author.id);
                    let authorWithBooks = { id: author.id, name: author.name, books: filteredBookByAuthor };
                    this.authorsWithBooks.push(authorWithBooks);
                }
                console.log('Auhtors list with books: ', this.authorsWithBooks);
            },
            info(item, index, button) {
                this.infoModal.title = `Row index: ${index}`
                this.infoModal.content = JSON.stringify(item, null, 2)
                this.$root.$emit('bv::show::modal', this.infoModal.id, button)
            },
            resetInfoModal() {
                this.infoModal.title = ''
                this.infoModal.content = ''
            },
            createAuthor() {
                console.log('Create Author');
            },
            myRowClickHandler(record, index) {
                console.log('myRowClickHandler', record);

                // this.info(record.item, record.index, $event.target)
                this.info(record, index);
            },
        },
    }
</script>