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
                <div>
                    <b-button size="sm" v-b-modal.modal-add-author >Add Author</b-button>

                    <!-- modal-add-author -->
                    <b-modal id="modal-add-author" title="Add New Author" hide-footer @hide="onHideModal">
                        <div>
                            <b-form @submit="onSubmitAddAuthor">
                              
                              <b-form-group id="input-group-1">
                                <b-form-input
                                  id="input-1"
                                  v-model="selectedRecord.name"
                                  placeholder="Enter name of the author"
                                  required
                                ></b-form-input>
                              </b-form-group>
                        
                              <b-button type="submit" variant="primary" class="float-right">Add</b-button>
                            </b-form>
                          </div>
                    </b-modal>

                    <!-- modal-edit-author -->
                    <b-modal id="modal-edit-author" title="Edit Author" hide-footer @hide="onHideModal" size="lg">
                        <div>                            
                            <b-form @submit="onSubmitEditAuthor">
                                <b-row>
                                    <b-col cols="9">                                    
                                        <b-form-group id="input-group-1">
                                            <b-form-input
                                                id="input-1"
                                                v-model="selectedRecord.name"
                                                placeholder="Enter name of the author"
                                                required
                                            ></b-form-input>                                        
                                        </b-form-group>                                    
                                    </b-col>                                
                                    <b-col cols="1">
                                        <b-button type="submit" variant="primary" class="float-left" size="sm">Save</b-button>
                                    </b-col>
                                    <b-col cols="1">
                                        <b-button variant="danger" size="sm" class="float-left" @click="deleteAuthor(selectedRecord.id)">Delete</b-button>
                                    </b-col>
                                </b-row>
                            </b-form>

                            <!-- book editor form, used for add and update of the book -->
                            <div class="pt-5">
                                <b-button size="sm" @click="showBookEditorHandler">Add Book</b-button>
                                <div v-if="showBookEditor" class="pt-2">
                                    <b-form @submit="onSubmitEditorBook">
                                        <b-row>
                                            <b-col cols="6">
                                                <b-form-group id="input-group-1">
                                                    <b-form-input
                                                        id="input-1"
                                                        v-model="selectedRecordBook.name"
                                                        placeholder="Enter name of the book"
                                                        required
                                                    ></b-form-input>
                                                </b-form-group>
                                            </b-col>
                                            <b-col cols="3">
                                                <b-form-group id="input-group-2">
                                                    <b-form-input
                                                        id="input-2"
                                                        v-model="selectedRecordBook.page_numbers"
                                                        type="number"
                                                        placeholder="Number of pages"
                                                        required
                                                    ></b-form-input>
                                                </b-form-group>
                                            </b-col>
                                            <b-col cols="3">
                                                <b-button size="sm" type="submit" variant="primary" class="float-left">Save</b-button>
                                            </b-col>
                                        </b-row>
                                    </b-form>
                                </div>
                            </div>

                            <div v-if="selectedRecord.books.length > 0" class="pt-3">
                                <b-table 
                                    small 
                                    hover 
                                    :items="selectedRecord.books"
                                    :fields="fieldsForBooks"
                                    @row-clicked="selectedBookTableRow"
                                >
                                    <template #cell(actions)="row">
                                        <div class="float-left">
                                            <b-button size="sm" @click="editBookItemModal(row.item)">Edit</b-button>
                                            <b-button variant="danger"  size="sm" @click="deleteBookItem(row.index)">Delete</b-button>
                                        </div>                                        
                                    </template>

                                </b-table>
                            </div>
                            <div v-else>
                                <b-row>
                                    <b-col cols="12">
                                        <p class="pt-2">No books registered for {{selectedRecord.name}}</p>
                                    </b-col>
                                </b-row>
                            </div>                 
                        </div>
                    </b-modal>
                </div>
            </b-col>
        </b-row>
        
        <!-- Authors table -->
        <b-table 
            small 
            hover
            :items="authorsWithBooks" 
            :fields="fields"
            :filter="filter"
            :filter-included-fields="filterOn"
            @row-clicked="selectedAuthorTableRow"
            :per-page="perPage"
            :current-page="currentPage"
            :busy="isBusyAuthorsTable"
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
    export default {
        middleware: 'auth',
        layout: 'navigation',
        name: 'AuthorsPage',
        data: () => ({
            perPage: 15,
            currentPage: 1,
            isBusyAuthorsTable: false,
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
            fieldsForBooks: [{
                    key: "id",
                    label: "Id"
                },
                {
                    key: "name",
                    label: "Name"
                },
                {
                    key: "page_numbers",
                    label: "Nr. pages"
                },
                {
                    key: "actions",
                    label: "Actions"
                }
            ],
            filter: null,
            filterOn: [],
            selectedRecord: {
                id: 0,
                name: null,
                books: []
            },
            selectedRecordBook: {
                id: 0,
                name: null,
                page_numbers: null,
                author_id: 0
            },
            showBookEditor: false,
            bookEditorType: 'ADD'
        }),
        computed: {
            rows() {
                return this.authorsWithBooks.length
            }
        },
        async mounted() {
            console.log('process.env.API_URL: ', process.env.API_URL);
            await this.loadDataFromDB();
        },
        methods: {
            async loadDataFromDB() {
                this.isBusyAuthorsTable = true;
                this.resetUI();

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

                this.isBusyAuthorsTable = false;
            },
            selectedAuthorTableRow(record) {
                this.selectedRecord = record;
                this.$bvModal.show('modal-edit-author');
            },
            async onSubmitAddAuthor(event) {
                event.preventDefault();
                // alert(JSON.stringify(this.form));

                await this.$axios.post('/authors/', {
                        id: this.selectedRecord.id,
                        name: this.selectedRecord.name
                    })
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });

                this.$bvModal.hide('modal-add-author'); // hide modal
                
                await this.loadDataFromDB(); // reload
            },
            async onSubmitEditAuthor(event) {
                event.preventDefault();

                await this.$axios.put(`/authors/${this.selectedRecord.id}`, {
                    id: this.selectedRecord.id,
                    name: this.selectedRecord.name
                    })
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });
                
                this.$bvModal.hide('modal-edit-author'); // hide modal

                await this.loadDataFromDB();
            },
            async deleteAuthor(selectedAuthorId) {
                await this.$axios.delete(`/authors/${selectedAuthorId}`)
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });

                this.$bvModal.hide('modal-edit-author'); // hide modal
                
                // this.selectedRecord.books.splice(selectedBookIndex, 1); // remove element at index (locally)
                await this.loadDataFromDB();
            },
            onHideModal() {
                this.resetUI();
            },
            resetUI() {
                this.selectedRecord = { id:0, name: null, books: [] }; // reset
                this.selectedRecordBook = { id: 0, name: null, page_numbers: null, author_id: 0 }; // reset
                this.showBookEditor = false;
                this.bookEditorType = 'ADD';
            },
            editBookItemModal(selectedBook) {
                // TODO: implement EDIT book by id

                // console.log('selectedBookTableRow', bookRecordToEdit);
                this.selectedRecordBook = selectedBook;

                this.showBookEditor = true;
                this.bookEditorType = 'EDIT';
            },
            async deleteBookItem(selectedBookIndex) {
                let bookRecordToDelete = this.selectedRecord.books.at(selectedBookIndex);
                // TODO: implement DELETE book by id

                await this.$axios.delete(`/books/${bookRecordToDelete.id}`)
                    .then(function (response) {
                        alert('SUCCESS');
                    })
                    .catch(function (error) {
                        console.log(error);
                        alert('FAILED');
                    });
                
                this.selectedRecord.books.splice(selectedBookIndex, 1); // remove element at index (locally)
            },
            showBookEditorHandler() {
                this.showBookEditor = !this.showBookEditor;

                this.selectedRecordBook = { id: 0, name: null, page_numbers: null, author_id: 0 }; // reset
                this.bookEditorType = 'ADD';
            },
            async onSubmitEditorBook(event) {
                event.preventDefault();
                // // alert(JSON.stringify(this.form));

                var responseBook = null;

                if (this.bookEditorType == 'ADD') {
                    const bookObjectToAdd = {
                        id: this.selectedRecordBook.id,
                        name: this.selectedRecordBook.name,
                        page_numbers: this.selectedRecordBook.page_numbers,
                        author_id: this.selectedRecord.id
                    };

                    await this.$axios.post('/books/', bookObjectToAdd)
                        .then(function (response) {
                            // console.log(response);
                            alert('SUCCESS');
                            responseBook = response.data;
                        })
                        .catch(function (error) {
                            console.log(error);
                            alert('FAILED');
                        });

                    // refresh the object locally
                    this.selectedRecord.books.push(responseBook);

                    // refresh local variables
                    this.selectedRecordBook = { id: 0, name: null, page_numbers: null, author_id: 0 }; // reset
                    this.showBookEditor = false;
                    this.bookEditorType = 'ADD';
                    
                    // await this.loadDataFromDB(); // reload
                } else if (this.bookEditorType == 'EDIT') {
                    // TODO: handle edit here

                    const bookObjectToUpdate= {
                        id: this.selectedRecordBook.id,
                        name: this.selectedRecordBook.name,
                        page_numbers: this.selectedRecordBook.page_numbers,
                        author_id: this.selectedRecordBook.author_id
                    };

                    await this.$axios.put(`/books/${bookObjectToUpdate.id}`, bookObjectToUpdate)
                        .then(function (response) {
                            // console.log(response);
                            alert('SUCCESS');
                            responseBook = response.data;
                        })
                        .catch(function (error) {
                            console.log(error);
                            alert('FAILED');
                        });

                    // refresh local variables
                    this.selectedRecordBook = { id: 0, name: null, page_numbers: null, author_id: 0 }; // reset
                    this.showBookEditor = false;
                    this.bookEditorType = 'ADD';
                }
            },
            selectedBookTableRow(bookRecord) {
                this.selectedRecordBook = bookRecord;

                this.showBookEditor = true;
                this.bookEditorType = 'EDIT';
            },
        },
    }
</script>
