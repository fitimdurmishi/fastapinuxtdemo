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
                                    <b-col cols="10">                                    
                                        <b-form-group id="input-group-1">
                                            <b-form-input
                                                id="input-1"
                                                v-model="selectedRecord.name"
                                                placeholder="Enter name of the author"
                                                required
                                            ></b-form-input>                                        
                                        </b-form-group>                                    
                                    </b-col>                                
                                    <b-col cols="2">
                                        <b-button type="submit" variant="primary" class="float-right">Update</b-button>
                                    </b-col>
                                </b-row>
                            </b-form>
                            <div v-if="selectedRecord.books.length > 0" class="pt-3">
                                <p>List of books</p>
                                <b-table 
                                    small 
                                    hover 
                                    :items="selectedRecord.books"
                                    :fields="fieldsForBooks"
                                >
                                    <template #cell(actions)="row">
                                        <div class="float-left">
                                            <b-button @click="editBookItemModal(row.item)">Edit</b-button>
                                            <b-button @click="deleteBookItem(row.index)">Delete</b-button>
                                        </div>                                        
                                    </template>

                                </b-table>
                            </div>
                            <div v-else>
                                No books for this author
                            </div>                 
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
            form: {
                id: 0,
                name: '',
            },
            selectedRecord: {
                id: 0,
                name: null,
                books: []
            }
        }),
        async mounted() {
            await this.loadDataFromDB();
        },
        methods: {
            async loadDataFromDB() {
                this.selectedRecord = { id:0, name: null, books: [] }; // reset

                let resAuthors = await this.$axios.get('http://127.0.0.1:8000/authors');
                let allAuthors = resAuthors.data;
                let resBooks = await this.$axios.get('http://127.0.0.1:8000/books/');
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
            myRowClickHandler(record) {
                console.log('myRowClickHandler', record);

                this.selectedRecord = record;
                // show modal with id: modal-edit-author
                // this.$root.$emit('bv::show::modal', 'modal-edit-author');
                this.$bvModal.show('modal-edit-author');
            },
            async onSubmitAddAuthor(event) {
                event.preventDefault();
                // alert(JSON.stringify(this.form));

                await this.$axios.post('http://127.0.0.1:8000/authors/', {
                    id: this.selectedRecord.id,
                    name: this.selectedRecord.name
                })
                .then(function (response) {
                    console.log(response);
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
                // alert(JSON.stringify(this.form));

                console.log('selectedRecord: ', this.selectedRecord.name);

                await this.$axios.put(`http://127.0.0.1:8000/authors/${this.selectedRecord.id}`, {
                    id: this.selectedRecord.id,
                    name: this.selectedRecord.name
                })
                .then(function (response) {
                    console.log(response);
                    alert('SUCCESS');
                })
                .catch(function (error) {
                    console.log(error);
                    alert('FAILED');
                });
                
                this.$bvModal.hide('modal-edit-author'); // hide modal

                await this.loadDataFromDB();
            },
            onHideModal() {
                console.log("onHideModal");
                this.selectedRecord = { id:0, name: null, books: [] }; // reset
            },
            editBookItemModal(selectedBook) {
                let bookRecordToEdit = selectedBook;
                console.log("bookRecordToEdit: ", bookRecordToEdit);
                // TODO: implement EDIT book by id
            },
            async deleteBookItem(selectedBookIndex) {
                let bookRecordToDelete = this.selectedRecord.books.at(selectedBookIndex);
                console.log("bookRecordToDelete: ", bookRecordToDelete);
                // TODO: implement DELETE book by id

                await this.$axios.delete(`http://127.0.0.1:8000/books/${bookRecordToDelete.id}`)
                .then(function (response) {
                    console.log(response);
                    alert('SUCCESS');                    
                })
                .catch(function (error) {
                    console.log(error);
                    alert('FAILED');
                });
                
                this.selectedRecord.books.splice(selectedBookIndex, 1); // remove element at index (locally)
            }
        },
    }
</script>
