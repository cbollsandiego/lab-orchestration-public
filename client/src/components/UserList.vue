<template>
    <div class="full-page">
    <div class="container">
        <alert :message="message" :isSuccess="alertSuccess" v-if="showMessage"></alert>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users">
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.role }}</td>
                    <td>
                        <button type="button" class="btn btn-danger btn-sm" @click="handleDeleteUser(user)">
                            Delete
                        </button>
                    </td>
                    <td>
                        <button type="button" class="btn btn-warning btn-sm" @click="toggleEditUserModal(user)">
                            Update
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    </div>
    <!-- edit modal-->
    <div ref="editUserModal" class="modal fade" :class="{ show: activeEditUserModal, 'd-block': activeEditUserModal }"
        tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Update</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"
                        @click="toggleEditUserModal">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="mb-3">
                            <label for="editUserRole" class="form-label">Role:</label>
                            <select class="form-control" id="editUserRole" v-model="editUserForm.role">
                                <option value="admin">
                                    Admin
                                </option>
                                <option value="instructor">
                                    Instructor
                                </option>
                                <option value="student">
                                    Student
                                </option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="editUserName" class="form-label">Name:</label>
                            <input type="text" class="form-control" id="editUserName" v-model="editUserForm.name"
                                placeholder="Enter name">
                        </div>
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-primary btn-sm" @click="handleEditSubmit">
                                Submit
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" @click="handleEditCancel">
                                Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
    <div v-if="activeEditUserModal" class="modal-backdrop fade show"></div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue'
export default {
    data() {
        return {
            users: [],
            showMessage: false,
            message: '',
            activeEditUserModal: false,
            alertSuccess: false,
            editUserForm: {
                name: '',
                role: '',
                id: '',
            },
        }
    },
    components: {
        alert: Alert,
    },
    methods: {
        getUsers() {
            const path = 'http://localhost:5001/userlist';
            let accessToken = localStorage.getItem('token')
            axios.get(path, {headers:{'Authorization': accessToken}})
                .then((res) => {
                    this.users = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        handleDeleteUser(user) {
            this.removeUser(user.id);
        },
        removeUser(userID) {
            const path = `http://localhost:5001/userlist/${userID}`;
            axios.delete(path)
                .then(() => {
                    this.getUsers();
                    this.message = 'User deleted!';
                    this.showMessage = true;
                    this.alertSuccess = true;
                })
                .catch((error) => {
                    console.error(error);
                    console.log("Got an error in remove users");
                    this.getUsers();
                });
        },
        toggleEditUserModal(user) {
            if (user) {
                this.editUserForm.role = user.role;
                this.editUserForm.name = user.name;
                this.editUserForm.id = user.id;
            }
            const body = document.querySelector('body');
            this.activeEditUserModal = !this.activeEditUserModal;
            if (this.activeEditUserModal) {
                body.classList.add('modal-open');
            } else {
                body.classList.remove('modal-open');
            }
        },
        handleEditSubmit() {
            this.toggleEditUserModal(null);
            let read = false;
            if (this.editUserForm.read) read = true;
            const payload = {
                role: this.editUserForm.role,
                name: this.editUserForm.name,
            };
            this.updateUser(payload, this.editUserForm.id);
        },
        updateUser(payload, userID) {
            const path = `http://localhost:5001/userlist/${userID}`;
            axios.put(path, payload)
                .then(() => {
                    this.getUsers();
                    this.message = 'User updated!';
                    this.showMessage = true;
                    this.alertSuccess = true;
                })
                .catch((error) => {
                    console.error(error);
                    this.getUsers();
                });
        },
        handleEditCancel() {
            this.toggleEditUserModal(null);
            this.initForm();
            this.getUsers();
        },
        initForm() {
            this.addUserForm.role = '';
            this.addUserForm.name = '';
            this.editUserForm.id = '';
        }
    },

    created() {
        this.getUsers();
    }
}
</script>

<style>

.form-switch .form-check-input {
  height: 20px;
  width: 48px;
}
.form-switch .form-check-input:focus {
  border-color: rgba(0, 0, 0, 0.25);
  outline: 0;
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba(0,0,0,0.25)'/></svg>");
}
.form-switch .form-check-input:checked {
  background-color: #4caf50;
  border-color: #4caf50;
  border: none;
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba(255,255,255,1.0)'/></svg>");
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.full-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f2f2f2;
  padding: 20px;
}

.title-container {
  width: 800px;
  text-align: center;
  margin-bottom: 20px;
}

.title {
  margin: 0;
}

.form-group {
  margin-bottom: 15px;
  width: 800px;
}

.input-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.question-label {
  flex-basis: 70px;
  font-weight: bold;
  margin-right: -12px;
}

.question {
  margin-bottom: 20px;
  position: relative;
}

.question-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 800px;
}

.question-content {
  display: flex;
  align-items: flex-start;
  width: 100%;
}

.question-order {
  flex-basis: 50px;
  font-weight: bold;
  font-size: 20px;
  margin-top: 34px;
}

.question-textarea-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.question-input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  height: 100px;
  resize: vertical;
  width: 100%;
}

.title-input {
  height: 32px;
  line-height: 32px;
}

.delete-question-wrapper {
  position: absolute;
  right: 0;
  bottom: -10px;
}

.delete-question {
  background-color: #ff0000;
  color: #fff;
  border: none;
  padding: 5px 8px;
  cursor: pointer;
  border-radius: 3px;
}

.add-question,
.create-lab-button {
  background-color: #4caf50;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.add-question {
  margin-bottom: 10px;
}

.create-lab-button {
  margin-bottom: auto;
  margin-top: 5px;
}

.question-order {
  flex-basis: 50px;
  font-weight: bold;
  font-size: 20px;
  margin-top: 34px;
  margin-right: -40px;
}

.btn-group-vertical {
  margin-top: 10px;
}
</style>