<template>
    <div>
      <form>
        <div class="mb-3">
            <label for="loginEmail" class="form-label">Email:</label>
            <input type="text" class="form-control" id="loginEmail" v-model="loginForm.email" placeholder="Enter Email">
        </div>
        <div>
            <button class="btn btn-primaty btn-sm" @click="handleLoginSubmit">Login</button>
        </div>
      </form>
    </div>
  </template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                alerts: [],
                loginForm: {
                    email: '',
                }
            };
        },

        methods: {
            handleLoginSubmit() {
                const payload = {
                    email: this.loginForm.email,
                };
                this.checkEmail(payload);
                this.initForm();
            },
            checkEmail(payload) {
                const path = 'http://localhost:5001/login';
                axios.post(path, payload)
                    .then(() => {
                        this.getLogin();
                    })
                    .catch((error) => {

                        console.log(error);
                        this.getLogin();
                    });
            },
            getLogin() {
                const path = 'http://localhost:5001/login';
                axios.get(path)
                    .then((res) => {
                        this.alerts = res.data.alerts;
                    })
                    .catch((error) => {
                        console.error(error);
                    });
            },
            initForm() {
                this.loginForm.email = '';
            },
        },
        created() {
            this.getLogin();
        },
    };
</script>
