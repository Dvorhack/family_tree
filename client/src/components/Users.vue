<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Family persons</h1>
        <hr><br><br>
<button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal>Add someone</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Family name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.first_name }}</td>
              <td>{{ user.last_name }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <b-modal ref="addUserModal"
            id="user-modal"
            title="Add a new user"
            hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                    label="First name:"
                    label-for="form-title-input">
        <b-form-input id="form-title-input"
                        type="text"
                        v-model="addUserForm.first_name"
                        required
                        placeholder="Enter first name">
        </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-group"
                    label="Last name:"
                    label-for="form-author-input">
            <b-form-input id="form-author-input"
                        type="text"
                        v-model="addUserForm.last_name"
                        required
                        placeholder="Enter last name">
            </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    </b-modal>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      addUserForm: {
        title: '',
        author: '',
      },
    };
  },
  methods: {
    getUsers() {
      const path = 'http://localhost:5000/get_users';
      axios.get(path)
        .then((res) => {
          this.users = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      console.log(this.users);
    },
    addBook(payload) {
      const path = 'http://localhost:5000/add_user';
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addUserForm.first_name = '';
      this.addUserForm.last_name = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      const payload = {
        first_name: this.addUserForm.first_name,
        last_name: this.addUserForm.last_name,
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
