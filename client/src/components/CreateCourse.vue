<template>
    <div class="full-page">
        <h1>Create Course</h1>
        <alert v-if="alertMessage" :message="alertMessage" :isSuccess="alertSuccess"></alert>
        <div class="input-text-box">
            <label>Name:</label>
            <input type="text" v-model="name" class="form-control">
        </div>
        <div class="input-text-box">
            <label>Semester:</label>
            <input type="text" v-model="semester" class="form-control">
        </div>
        <div class="input-text-box">
            <label>Section:</label>
            <input type="number" v-model="section" class="form-control" min="1" max="99">
        </div>
        <div class="input-text-box">
            <label>Instructor name:</label>
            <input type="text" v-model="instructor" class="form-control" list="instructorList">
            <datalist id="instructorList">
                <option v-for="instructor in instructorOptions" :value="instructor.name"></option>
            </datalist>
        </div>
        <br>
        <button @click="createCourse" class="create-course-button">Create Course</button>
    </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue'
export default {
    data() {
        return {
            name: '',
            semester: '',
            section: 1,
            instructor: '',
            instructorOptions: [],
            alertMessage: "",
            alertSuccess: false
        }
    },
    components: {
        alert: Alert
    },
    mounted() {
        const path = 'http://localhost:5001/newcourse/getinstructors'
        axios.get(path)
        .then((res) => {
            this.instructorOptions = res.data;
        })
        .catch((error) => {
            console.log(error)
        })
    },
    methods: {
        createCourse() {
            console.log('yeah yeah awesome')
            const path = 'http://localhost:5001/newcourse/submit'
            const newCourse = {'name': this.name, 'semester': this.semester, 'section': this.section, 'instructor': this.instructor}
            axios.post(path, newCourse)
                .then((response) => {
                    if(response.data.status === 'exists') {
                        this.alertMessage = 'Course already exists. Change name, semester, or section number'
                        this.alertSuccess = false
                    }
                    else if(response.data.status === 'noprof') {
                        this.alertMessage = 'Instructor not found in database.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'noname') {
                        this.alertMessage = 'Course name required.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'nosem') {
                        this.alertMessage = 'Semester required.'
                        this.alertSuccess = false
                    }
                    else if (response.data.status === 'nosec') {
                        this.alertMessage = 'Invalid Section Number.'
                        this.alertSuccess = false
                    }
                    else {
                        this.alertMessage = 'Course successfully created.'
                        this.alertSuccess = true
                        this.name = ''
                        this.semester = ''
                        this.section = 1
                        this.instructor = ''
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
}
</script>
