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
            <select  class= "form-control" name="roles" id="roles">
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

            axios.post(path, newUser)
                .then((response) => {
                    if (response.data.status === 'exists') {
                        this.alertMessage = 'User already exists. Change name, id, or email'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'noname') {
                        this.alertMessage = 'Name not found in database.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'nopassword') {
                        this.alertMessage = 'Password required.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'nosem') {
                        this.alertMessage = ' Email required.'
                        this.alertSuccess = false

                    }
                    else {
                        this.alertMessage = 'User successfully created.'
                        this.alertSuccess = true
                        this.name = ''
                        this.id = ''
                        this.email = ''
                        this.role = ''
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
}
</script>


<style scoped>
.create-user-button {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
}

html,
body {
    height: 100%;
    margin: 0;
    padding: 0;
}

.full-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f2f2f2;
    padding: 20px;
}

.input-text-box {
    padding: 10px;
    width: 740px;
}
</style>


For the role, there are only four choices: admin, instructor, 
lab assistant, and student. 
I would suggest using a drop down for these choices then. 

You will have to change the routes for the page
the other change that needs to be made to your lab page is to
 pull the lab from the database instead of having it hardcoded


