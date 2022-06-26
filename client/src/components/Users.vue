<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Family persons</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage"></alert>
<button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal>Add someone</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" v-for="(item, key, index) in users[0]" :key="index">{{key}}</th>
              <!-- <th scope="col">Family name</th> -->
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <!-- <td>{{ user.first_name }}</td>
              <td>{{ user.last_name }}</td> -->
              <td v-for="(item, key, index) in user" :key="index">{{item}}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm"
                  v-b-modal.user-update-modal
                  @click="editUser(user)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  @click="onDeleteUser(user)">Delete</button>
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
    <b-modal ref="editUserModal"
         id="user-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="First name:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editForm.first_name"
                    required
                    placeholder="Enter first name">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-edit-group"
                  label="Last name:"
                  label-for="form-author-edit-input">
        <b-form-input id="form-author-edit-input"
                      type="text"
                      v-model="editForm.last_name"
                      required
                      placeholder="Enter last name">
        </b-form-input>
      </b-form-group>
    <b-button-group>
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-button-group>
  </b-form>
</b-modal>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      users: [],
      addUserForm: {
        first_name: '',
        last_name: '',
      },
      editForm: {
        user_id: '',
        first_name: '',
        last_name: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getUsers() {
      const path = 'http://localhost:5000/users';
      axios.get(path)
        .then((res) => {
          this.users = res.data.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      console.log(this.users);
    },
    removeUser(userID) {
      const path = `http://localhost:5000/users/${userID}`;
      axios.delete(path)
        .then(() => {
          this.getUsers();
          this.message = 'User removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
          this.getUsers();
        });
    },
    onDeleteUser(user) {
      this.removeUser(user.user_id);
    },
    addUser(payload) {
      const path = 'http://localhost:5000/users';
      axios.post(path, payload)
        .then(() => {
          this.getUsers();
          this.message = 'User added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getUsers();
        });
    },
    editUser(user) {
      console.log(user);
      this.editForm = user;
    },
    initForm() {
      this.addUserForm.first_name = '';
      this.addUserForm.last_name = '';
      this.editForm.user_id = '';
      this.editForm.first_name = '';
      this.editForm.last_name = '';
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      const payload = {
        first_name: this.editForm.first_name,
        last_name: this.editForm.last_name,
      };
      this.updateUser(payload, this.editForm.user_id);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editUserModal.hide();
      this.initForm();
      this.getUsers(); // why?
    },
    updateUser(payload, bookID) {
      console.log(payload);
      const path = `http://localhost:5000/users/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
          this.getUsers();
        });
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      const payload = {
        first_name: this.addUserForm.first_name,
        last_name: this.addUserForm.last_name,
      };
      this.addUser(payload);
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
