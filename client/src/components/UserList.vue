<template>
    <div class="container">
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
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                users: []
            }
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
        created() { 
            this.getUsers();
        }
    }
</script>