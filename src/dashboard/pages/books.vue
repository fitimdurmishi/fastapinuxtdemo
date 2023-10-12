<template>
    <b-container fluid class="p-5">

        <b-row>
            <b-col cols="6" class="mb-2">
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
            <b-col cols="6" class="mb-2 text-right">
                <div>
                    <b-button size="sm" v-b-modal.modal-add-book >Add Book</b-button>

                    <!-- modal-add-book -->
                    <b-modal id="modal-add-book" title="Add New Book" hide-footer @hide="onHideModal">
                        <div>
                            <b-form @submit="onSubmitAddBook">
                              
                                <b-form-group id="input-group-1">
                                    <b-form-input
                                        id="input-1"
                                        v-model="selectedRecordBook.name"
                                        placeholder="Enter name of the book"
                                        required
                                    ></b-form-input>
                                </b-form-group>
                                <b-form-group id="input-group-2">
                                    <b-form-input
                                        id="input-2"
                                        v-model="selectedRecordBook.page_numbers"
                                        type="number"
                                        placeholder="Number of pages"
                                        required
                                    ></b-form-input>
                                </b-form-group>
                                
                                <treeselect 
                                    v-model="selectedRecordBook.author.id" 
                                    :multiple="false" 
                                    :options="authorOptions"
                                    placeholder="Select an author" 
                                />                            
                        
                                <b-button type="submit" variant="primary" class="float-right mt-2">Add</b-button>
                            </b-form>

                          </div>
                    </b-modal>

                    <!-- TODO -->
                    <!-- modal-edit-book -->
                    <b-modal id="modal-edit-book" title="Edit Book" hide-footer @hide="onHideModal">
                        <div>                            
                            <b-form @submit="onSubmitEditBook">
                                <b-row>
                                    <b-col cols="12">                                    
                                        <b-form-group id="input-group-1">
                                            <b-form-input
                                                id="input-1"
                                                v-model="selectedRecordBook.name"
                                                placeholder="Enter name of the book"
                                                required
                                            ></b-form-input>                                        
                                        </b-form-group>
                                        <b-form-group id="input-group-2">
                                            <b-form-input
                                                id="input-2"
                                                v-model="selectedRecordBook.page_numbers"
                                                type="number"
                                                placeholder="Number of pages"
                                                required
                                            ></b-form-input>
                                        </b-form-group>
                                        
                                        <treeselect 
                                            v-model="selectedRecordBook.author.id" 
                                            :multiple="false" 
                                            :options="authorOptions"
                                            placeholder="Select an author" 
                                        />
                                    </b-col>                                
                                    <b-col cols="12">
                                        <div class="float-right pt-3">
                                            <b-button type="submit" variant="primary" size="sm">Save</b-button>
                                            <b-button variant="danger" size="sm" class="ml-2" @click="deleteBook(selectedRecordBook.id)">Delete</b-button>
                                        </div>                                        
                                    </b-col>
                                </b-row>
                            </b-form>                
                        </div>
                    </b-modal>
                </div>
            </b-col>
        </b-row>

        <!-- Books table -->
        <!-- @row-clicked="selectedBookTableRow" -->
        <b-table 
            small 
            hover
            :items="booksWithAuthorsDetails" 
            :fields="fieldsForBooks"
            :filter="filter"
            :filter-included-fields="filterOn"
            :per-page="perPage"
            :current-page="currentPage"
            :busy="isBusyBooksTable"
            @row-clicked="selectedBookTableRow"
        >
            <template #table-busy>
                <div class="text-center my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Loading...</strong>
                </div>
            </template>
        </b-table>

        <b-pagination
            v-model="currentPage"
            size="sm"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
        >
        </b-pagination>
        <p class="mt-3">Current Page: {{ currentPage }} [{{ perPage }} rows per page]</p>
    </b-container>
</template>

<script>
    import Treeselect from '@riophae/vue-treeselect'
    import '@riophae/vue-treeselect/dist/vue-treeselect.css'

    export default {
        middleware: 'auth',
        components: { Treeselect },
        layout: 'Navigation',
        name: 'BooksPage',
        data: () => ({
            booksWithAuthorsDetails: [],
            allAuthors: [],
            authorOptions: [], // options for treeselect
            isClient: false, // Flag to check if running on the client (VueTreeselect related only),
            perPage: 15,
            currentPage: 1,
            isBusyBooksTable: false,            
            fieldsForBooks: [
                {
                    key: "id",
                    label: "Id"
                },
                {
                    key: "name",
                    label: "Name"
                },
                {
                    key: "author.name",
                    label: "Author"
                },
                {
                    key: "page_numbers",
                    label: "Nr. pages"
                },
            ],
            filter: null,
            filterOn: [],
            selectedRecordBook: {
                id: 0,
                name: null,
                page_numbers: null,
                author: {
                    id: null,
                    name: null
                }
            },
        }),
        computed: {
            rows() {
                return this.booksWithAuthorsDetails.length;
            }
        },
        // async mounted() {
        //     await this.loadDataFromDB();
        //     console.log('booksWithAuthorsDetails: ', this.booksWithAuthorsDetails);
        //     console.log('allAuthors: ', this.allAuthors);
        // },
        async created() {
            this.isClient = process.client; // Set isClient based on client-side or server-side

            await this.loadDataFromDB();
        },
        methods: {
            async loadDataFromDB() {
                this.isBusyBooksTable = true;
                this.resetUI();

                let resAuthors = await this.$axios.get('/authors');
                this.allAuthors = resAuthors.data;
                let resBooks = await this.$axios.get('/books/');
                let allBooks = resBooks.data;

                // Convert the fetched authors to the format expected by Vue-Treeselect
                if (this.isClient) {
                    this.authorOptions = this.allAuthors.map((author) => ({
                        id: author.id,
                        label: author.name, // Assuming 'name' is the property with the author's name
                    }));
                }

                this.booksWithAuthorsDetails = [];
                for (let i = 0; i < allBooks.length; i++) {
                    let book = allBooks[i];
                    let authorForThisBook = this.allAuthors.filter(a => a.id == book.author_id)[0]; // get the first element
                    let bookWithAuthorsDetails = { id: book.id, name: book.name, page_numbers: book.page_numbers, author: authorForThisBook };
                    this.booksWithAuthorsDetails.push(bookWithAuthorsDetails);
                }

                this.isBusyBooksTable = false;
            },
            selectedBookTableRow(record) {
                this.selectedRecordBook = record;

                this.$bvModal.show('modal-edit-book');
            },
            onHideModal() {
                this.resetUI();
            },
            resetUI() {
                this.selectedRecordBook = { id: 0, name: null, page_numbers: null, author: { id:null, name: null} }; // reset
            },
            async onSubmitAddBook(event) {
                event.preventDefault();
                // alert(JSON.stringify(this.form));

                await this.$axios.post('/books/', {
                        id: this.selectedRecordBook.id,
                        name: this.selectedRecordBook.name,
                        page_numbers: this.selectedRecordBook.page_numbers,
                        author_id: this.selectedRecordBook.author.id
                    })
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });

                this.$bvModal.hide('modal-add-book'); // hide modal
                
                await this.loadDataFromDB(); // reload
            },
            async onSubmitEditBook(event) {
                event.preventDefault();

                await this.$axios.put(`/books/${this.selectedRecordBook.id}`, {
                        id: this.selectedRecordBook.id,
                        name: this.selectedRecordBook.name,
                        page_numbers: this.selectedRecordBook.page_numbers,
                        author_id: this.selectedRecordBook.author.id
                    })
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });

                this.$bvModal.hide('modal-edit-book'); // hide modal

                await this.loadDataFromDB();
            },
            async deleteBook(selectedBookId) {
                await this.$axios.delete(`/books/${selectedBookId}`)
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });

                this.$bvModal.hide('modal-edit-book'); // hide modal
                
                await this.loadDataFromDB();
            },
        },
    }
</script>