<template>
    <div class="container">
        <alert :message="message" v-if="showMessage"></alert>
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
            axios.get(path)
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