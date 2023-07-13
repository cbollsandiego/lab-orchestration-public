<template>
    <h1>Create Lab</h1>
    <alert v-if="alertMessage" :message="alertMessage" :isSuccess="alertSuccess"></alert>
    <label>Name:</label>
    <input type="text" v-model="name" class="form-control">
    <label>Semester:</label>
    <input type="text" v-model="semester" class="form-control">
    <label>Section:</label>
    <input type="number" v-model="section" class="form-control" min="1" max="99">
    <label>Instructor name:</label>
    <input type="text" v-model="instructor" class="form-control" list="instructorList">
    <datalist id="instructorList">
        <option v-for="instructor in instructorOptions" :value="instructor.name"></option>
    </datalist>
    <br>
    <button @click="createCourse" class="create-course-button">Create Course</button>
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
            instructorOptions: []
        }
    },
    components: {
        alert: Alert
    },
    mounted() {
        const path = 'http://localhost:5001/newcourse/getinstructors'
        axios.get(path)
        .then((res) => {
            console.log(res.data)
            this.instructorOptions = res.data;
        })
        .catch((error) => {
            console.log(error)
        })
    },
    methods: {
        createCourse() {
            const path = 'http://localhost:5001/newcourse/submit'
        }
    }
}
</script>

<style>
.create-course-button {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
  }
</style>