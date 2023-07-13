<template>
    <div> 
        <div v-if="message!=''">
            <alert :message="message"></alert>
        </div>
      <form>
        <div class="mb-3">
            <label for="loginEmail" class="form-label">Email:</label>
            <input type="text" class="form-control" id="loginEmail" v-model="loginForm.email" placeholder="Enter Email">
            <label for="loginPass" class="form-label">Password:</label>
            <input type="text" class="form-control" id="loginPass" v-model="loginForm.pass" placeholder="Enter Password">
        </div>
        <div>
            <button class="btn btn-primaty btn-sm" @click="handleLoginSubmit">Login</button>
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
                        this.alerts.push('Logged in!')
                        localStorage.setItem('token', response.data.token)
                        console.log(response.data)
                    })
                    .catch((error) => {
                        console.log(error);
                    });
            },
            initForm() {
                this.loginForm.email = '';
            },
        },
    };
</script>
