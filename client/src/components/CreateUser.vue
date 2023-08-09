<template>
    <div class="full-page">
        <h1>Create User</h1>
        <alert v-if="alertMessage" :message="alertMessage" :isSuccess="alertSuccess"></alert>
        <div class="input-text-box">
            <label>Name:</label>
            <input type="text" v-model="name" class="form-control">
        </div>
        <div class="input-text-box">
            <label>Password:</label>
            <input type="text" v-model="password" class="form-control">
        </div>
        <div class="input-text-box">
            <label>Email:</label>
            <input type="text" v-model="email" class="form-control">
        </div>
        <div class="input-text-box">
           <label> Role:</label><br>
            <select v-model="role" class="form-control" name="roles" id="roles">
                <option value="student" >Student</option>
                <option value="instructor" >Instructor</option>
                <option value="admin" >Admin</option>
                <option value="lab assistant" >Lab assistant</option>
            </select> <br>
            <button @click="createUser" class="create-user-button">Create User</button>
        </div>
    </div>
    <br>
    
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue'
export default {
    data() {
        return {
            name: '',
            password: '',
            email: '',
            role: '',
            alertMessage: "",
            alertSuccess: false
        }
    },
    components: {
        alert: Alert
    },
    methods: {
        createUser() {
            console.log('yeah yeah awesome')
            const path = 'http://localhost:5001/createuser'
            const newUser = { 'password': this.password, 'name': this.name, 'email': this.email, 'role': this.role }
            const accessToken= localStorage.getItem("token")

            axios.post(path, newUser, {headers:{"Authorization":accessToken}})
                .then((response) => {
                    if (response.data.status === 'exists') {
                        this.alertMessage = 'User already exists. Change name, id, or email'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'noname') {
                        this.alertMessage = 'Name required.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'nopassword') {
                        this.alertMessage = 'Password required.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'noemail') {
                        this.alertMessage = ' Email required.'
                        this.alertSuccess = false

                    }
                    else if (response.data.status === 'norole') {
                        this.alertMessage = ' Role required.'
                        this.alertSuccess = false
                    }
                    else {
                        this.alertMessage = 'User successfully created.'
                        this.alertSuccess = true
                        this.name = ''
                        this.password = ''
                        this.email = ''
                        this.role = ''
                    }
                })
                .catch((error) => {
                    console.log(error)
                    this.$router.push({ name: 'Login'})
                })
        }
    }
}
</script>






