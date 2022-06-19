<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Family persons</h1>
        <hr><br><br>
        <alert :message="message" v-if="showMessage"></alert>
<button type="button" class="btn btn-success btn-sm" v-b-modal.link-modal>Add link</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col" v-for="(item, key, index) in links[0]" :key="index">{{key}}</th>
              <!-- <th scope="col">Family name</th> -->
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(link, index) in links" :key="index">
              <!-- <td>{{ link.base_user }}</td>
              <td>{{ link.dest_user }}</td> -->
              <td v-for="(item, key, index) in link" :key="index">{{item}}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm"
                  v-b-modal.link-update-modal
                  @click="editlink(link)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm"
                  @click="onDeletelink(link)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <b-modal ref="addlinkModal"
            id="link-modal"
            title="Add a new link"
            hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                    label="Base user:"
                    label-for="form-title-input">
        <b-form-select v-model="selected" :options="users"></b-form-select>
        <!-- <b-form-input id="form-title-input"
                        type="text"
                        v-model="addlinkForm.base_user"
                        required
                        placeholder="Enter first name">
        </b-form-input> -->
        </b-form-group>
        <b-form-group id="form-title-group"
                    label="Lien de parenté:"
                    label-for="form-title-input">
        <b-form-select v-model="selected" :options="parente"></b-form-select>
        </b-form-group>
        <b-form-group id="form-author-group"
                    label="Dest user:"
                    label-for="form-author-input">
                    <b-form-select v-model="selected" :options="users"></b-form-select>
            <!-- <b-form-input id="form-author-input"
                        type="text"
                        v-model="addlinkForm.dest_user"
                        required
                        placeholder="Enter last name">
            </b-form-input> -->
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    </b-modal>
    <b-modal ref="editlinkModal"
         id="link-update-modal"
         title="Update"
         hide-footer>
  <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
  <b-form-group id="form-title-edit-group"
                label="First name:"
                label-for="form-title-edit-input">
      <b-form-input id="form-title-edit-input"
                    type="text"
                    v-model="editForm.base_user"
                    required
                    placeholder="Enter first name">
      </b-form-input>
    </b-form-group>
    <b-form-group id="form-author-edit-group"
                  label="Last name:"
                  label-for="form-author-edit-input">
        <b-form-input id="form-author-edit-input"
                      type="text"
                      v-model="editForm.dest_user"
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
      links: [],
      users: [],
      addlinkForm: {
        base_user: '',
        dest_user: '',
      },
      parente: ['conjoint de', 'parent de'],
      editForm: {
        link_id: '',
        base_user: '',
        dest_user: '',
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
          console.log(res.data.users.length);
          for (let i = 0; i < res.data.users.length; i += 1) {
            console.log(res.data.users[i].first_name);
            this.users.push(res.data.users[i].first_name);
          }
          // this.users = res.data.users;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      console.log(this.users);
    },
    getlinks() {
      const path = 'http://localhost:5000/links';
      axios.get(path)
        .then((res) => {
          this.links = res.data.links;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      console.log(this.links);
    },
    removelink(linkID) {
      const path = `http://localhost:5000/links/${linkID}`;
      axios.delete(path)
        .then(() => {
          this.getlinks();
          this.message = 'link removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
          this.getlinks();
        });
    },
    onDeletelink(link) {
      this.removelink(link.link_id);
    },
    addlink(payload) {
      const path = 'http://localhost:5000/links';
      axios.post(path, payload)
        .then(() => {
          this.getlinks();
          this.message = 'link added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getlinks();
        });
    },
    editlink(link) {
      console.log(link);
      this.editForm = link;
    },
    initForm() {
      this.addlinkForm.base_user = '';
      this.addlinkForm.dest_user = '';
      this.editForm.link_id = '';
      this.editForm.base_user = '';
      this.editForm.dest_user = '';
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editlinkModal.hide();
      const payload = {
        base_user: this.editForm.base_user,
        dest_user: this.editForm.dest_user,
      };
      this.updatelink(payload, this.editForm.link_id);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editlinkModal.hide();
      this.initForm();
      this.getlinks(); // why?
    },
    updatelink(payload, bookID) {
      console.log(payload);
      const path = `http://localhost:5000/links/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getlinks();
        })
        .catch((error) => {
          // eslint-disable-next-line
            console.error(error);
          this.getlinks();
        });
    },

    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addlinkModal.hide();
      const payload = {
        base_user: this.addlinkForm.base_user,
        dest_user: this.addlinkForm.dest_user,
      };
      this.addlink(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addlinkModal.hide();
      this.initForm();
    },
  },
  created() {
    this.getlinks();
    this.getUsers();
  },
};
</script>
