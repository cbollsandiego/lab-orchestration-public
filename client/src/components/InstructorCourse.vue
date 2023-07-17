<template>
    <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
    <h1>{{this.name}}</h1>
    <h2>{{this.instructor}}</h2>
    <h3>Sessions</h3>
    <ul class="list-group list-group-flush all">
        <router-link v-for="session in sessions" :to="{name: 'Live Session', params: {sessionId: session.id}}" class="route-link">
            <li class="list-group-item">{{session.name}} {{session.lab_name}}</li>
        </router-link>
    </ul>
    <div class="input-text-box">
        <label>Add session:</label>
        <input type="text" v-model="newSessionName" class="form-control" placeholder="New Session Name">
    </div>
    <select v-model="newSessionLab">
        <option disabled value="">Choose Lab</option>
        <option v-for="lab in labs">{{lab.title}}</option>
    </select>
    <button @click="addSession" class="create-session">Create Session</button>
    <br>
    <h3>Members</h3>
    <div class="custom-file">
        <h5>Add Students From File:</h5>
        <input type="file" class="custom-file-input" id="customFile" @change="addFromFile($event)">
    </div>
    <div class="input-text-box">
        <label>Add student by name:</label>
        <input type="text" v-model="newMemberName" class="form-control" placeholder="New Student Name">
    </div>
    <button @click="addFromName" class="add-from-name">Add Student</button>
    <br>
    <ul class="list-group list-group-flush">
        <li v-for="member in members" class="list-group-item">{{member.name}}</li>
    </ul>
    <select v-model="memberToRemove">
        <option disabled value="">Select student to remove</option>
        <option v-for="member in members">{{member.name}}</option>
    </select>
    <button @click="removeStudent(memberToRemove)" class="remove-student">Remove</button>
</template>

<script>
import axios from 'axios'
import Alert from './Alert.vue'
export default {
    data() {
        return {
            name: '',
            instructor: '',
            members: [],
            sessions: [],
            labs: [],
            newSessionName: '',
            newSessionLab: '',
            memberToRemove: '',
            newMemberName: '',
            addFile: null,
            alertMessage: '',
            alertSuccess: false,
        }
    },
    props: {
        currentUserRole: {type: String}
    },
    components: {
        Alert
    },
    created() {
        this.getInfo()
    },
    methods: {
        getInfo() {
            const path = `http://localhost:5001/getcourse/instructor/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            axios.get(path, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.name = res.data.name
                        this.instructor = res.data.instructor
                        this.members = res.data.members
                        this.sessions = res.data.sessions
                        this.labs = res.data.labs
                    }
                    
                })
                .catch((error) => {
                    console.log(error)
                })
            window.scrollTo(0,0)
        },
        async removeStudent(studentToRemove) {
            if(!studentToRemove){
                this.alertMessage = 'Select a student to remove'
                this.alertSuccess = false
                return;
            }
            const path = `http://localhost:5001/removefromcourse/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            await axios.post(path, {'student_name': studentToRemove}, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.alertMessage = studentToRemove + ' removed from course.'
                        this.alertSuccess = true
                    }
                    else {
                        this.alertMessage = 'Failed to remove ' + studentToRemove
                        this.alertSuccess = false
                    }
                })
                .catch((error) => {
                    this.alertMessage = 'Failed to remove ' + studentToRemove
                    this.alertSuccess = false
                    console.log(error)
                })
            this.getInfo()
        },
        async addSession() {
            if(!this.newSessionLab || !this.newSessionName) {
                this.alertMessage = 'Select a lab and choose a valid session name'
                this.alertSuccess = false
                return;
            }
            const path = `http://localhost:5001/addsession/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            await axios.post(path, {'lab': this.newSessionLab, 'name': this.newSessionName.trim()}, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.alertMessage = 'Added new session'
                        this.alertSuccess = true
                        this.newSessionLab = null
                        this.newSessionName = ''
                    }
                    else {
                        this.alertMessage = 'Failed to add new session'
                        this.alertSuccess = false
                    }
                })
                .catch((error) => {
                    console.log(error)
                    this.alertMessage = 'Failed to add new session'
                    this.alertSuccess = false
                })
            this.getInfo()
        },
        async addFromFile(event) {
            const file = event.target.files[0]
            console.log(file)
            if(file.type != 'text/csv') {
                this.alertMessage = 'Invalid file type. Try again.'
                this.alertSuccess = false
                return;
            }
            const path = `http://localhost:5001/addfromfile/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            await axios.post(path, {'file': file}, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.alertMessage = 'Added all students from file'
                        this.alertSuccess = true
                    }
                    else {
                        this.alertMessage = 'Failed to add from file. Check that your file is correct.'
                        this.alertSuccess = false
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        async addFromName() {
            if(!this.newMemberName){
                this.alertMessage = 'Enter the new student\'s name'
                this.alertSuccess = false
                return;
            }
            const path = `http://localhost:5001/addfromname/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            await axios.post(path, {'student_name': this.newMemberName.trim()}, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.alertMessage = this.newMemberName + ' added to course.'
                        this.alertSuccess = true
                        this.newMemberName = ''
                    }
                    else {
                        this.alertMessage = 'Failed to add ' + this.newMemberName
                        this.alertSuccess = false
                    }
                })
                .catch((error) => {
                    this.alertMessage = 'Failed to add ' + this.newMemberName
                    this.alertSuccess = false
                    console.log(error)
                })
            this.getInfo()
        }
    }
}
</script>

<style>
.remove-student {
    background-color: #ff0000;
    color: #fff;
    border: none;
    padding: 5px 8px;
    cursor: pointer;
    border-radius: 3px;
}

.add-from-name,
.create-session {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
}

.all {
    width: 800px;
  }
</style>