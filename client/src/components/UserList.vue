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
                    <td>{{user.name}}</td> 
                    <td>{{user.email}}</td>
                    <td>{{user.role}}</td>
                    <td><button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="handleDeleteUser(user)">
                        Delete
                    </button></td>
                </tr>
            </tbody>
        </table>
    </div>
    [...]
      <div class="text-center">
        <button type="button" class="btn text-white my-4" @click="$emit('deleteUser')">Delete account</button>
      </div>
    [...]
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
                    this.users=res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            }
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
                    this.getUsers();
                });
        },
        created() { 
            this.getUsers();
        }
    }
</script>