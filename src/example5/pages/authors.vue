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
                        >
                        </b-form-input>
            
                        <b-input-group-append>
                        <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                        </b-input-group-append>
                    </b-input-group>
                </b-form-group>
            </b-col>
            <b-col lg="6" class="mb-2 text-right">
                <!-- <b-button size="sm" v-on:click="createAuthor">Create Author</b-button> -->
                <div>
                    <b-button size="sm" v-b-modal.modal-add-author>Add Author</b-button>
                    <b-modal id="modal-add-author" title="Add New Author" ok-only>
                        <div>
                            <b-form @submit="onSubmit" @reset="onReset">
                              
                              <b-form-group id="input-group-2" label="Author Name:" label-for="input-2">
                                <b-form-input
                                  id="input-2"
                                  v-model="form.name"
                                  placeholder="Enter name of the author"
                                  required
                                ></b-form-input>
                              </b-form-group>
                        
                              <b-button type="submit" variant="primary">Submit</b-button>
                              <b-button type="reset" variant="danger">Reset</b-button>
                            </b-form>
                          </div>
                    </b-modal>
                  </div>
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
        </b-table>

        <!-- Info modal -->
        <b-modal :id="infoModal.id" :title="infoModal.title" ok-only @hide="resetInfoModal">
            <pre>{{ infoModal.content }}</pre>
        </b-modal>
    </b-container>
</template>

<script>
    export default {
        components: {
        },
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
            form: {
                id: 0,
                name: '',
            },
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
                // this.infoModal.title = `Row index: ${index}`
                this.infoModal.title = `Edit: ${item.name}`
                this.infoModal.content = JSON.stringify(item, null, 2)
                this.$root.$emit('bv::show::modal', this.infoModal.id, button)
            },
            resetInfoModal() {
                this.infoModal.title = ''
                this.infoModal.content = ''
            },
            myRowClickHandler(record, index) {
                console.log('myRowClickHandler', record);

                // this.info(record.item, record.index, $event.target)
                this.info(record, index);

                // this.dialogType = "EDIT";
                // this.modalVisible = true;
            },
            createAuthor() {
                console.log("createAuthor");
            },
            onSubmit(event) {
                event.preventDefault()
                alert(JSON.stringify(this.form))
            },
            onReset(event) {
                event.preventDefault()
                // Reset our form values
                this.form.name = '';
                // Trick to reset/clear native browser form validation state
                this.show = false;
                this.$nextTick(() => {
                    this.show = true
                })
            },
        },
    }
</script>