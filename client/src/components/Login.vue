<template>
    <div>
        <div v-if="message != ''">
            <alert :message="message"></alert>
        </div>
        <form>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
            <div class="mb-3">
                <label for="loginEmail" class="form-label">Email:</label>
                <input type="text" class="form-control" id="loginEmail" v-model="loginForm.email" placeholder="Enter Email" @keyup.enter="handleLoginSubmit">
                <label for="loginPass" class="form-label">Password:</label>
                <input type="text" class="form-control" id="loginPass" v-model="loginForm.pass"
                    placeholder="Enter Password" @keyup.enter="handleLoginSubmit">
            </div>
            <div>
                <button type="button" class="btn btn-outline-success" @click="handleLoginSubmit">Login</button>
            </div>
        </form>
    </div>
</template>

<script>
    import axios from 'axios';
    import Alert from './Alert.vue';
    export default {
        data() {
            return {
                message: "",
                loginForm: {
                    email: '',
                    pass: ''
                }
            };
        },
        components:{
            alert:Alert,
        },
        methods: {
            handleLoginSubmit() {
                const payload = {
                    email: this.loginForm.email,
                    pass: this.loginForm.pass
                };
                this.checkEmail(payload);
                this.initForm();
            },
            checkEmail(payload) {
                const path = 'http://localhost:5001/login';
                axios.post(path, payload)
                    .then((response) => {
                        if(response.data.status === 'failure') {
                            this.message = 'Incorrect username or password.'
                        }
                        else {
                            this.message = 'Logged in!'
                            localStorage.setItem('token', response.data.token)
                            localStorage.setItem('role', response.data.role)
                            this.$router.push({ name: 'My Courses'})
                        }
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            initForm() {
                this.loginForm.pass = '';
            },
        },
    }
</script>
