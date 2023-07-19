<template>
    <div class="container">
        <h1>My Courses</h1>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Course Name</th>
                    <th>Semester</th>
                    <th>Section</th>
                    <th>Instructor</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="course in courses">
                    <td>{{course.id}}</td> 
                    <td>
                        <router-link 
                        :to="{name: 'Course', params: 
                        {course_name: course.course_name, semester: course.semester, section: course.section_num}}" 
                        class="Course">
                        {{course.course_name}}
                        </router-link>
                    </td>
                    <td>{{course.semester}}</td>
                    <td>{{course.section_num}}</td>
                    <td>{{course.course_instructor}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            courses: []
        }
    },
    methods: {
        getMyCourses() {
            const path = 'http://localhost:5001/mycourses'
            let accessToken = localStorage.getItem('token')
            console.log('okay, yeah')
            axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.courses = res.data
            })
            .catch((error) => {
                console.log(error)
                this.$router.push({ name: 'Login'})
            })
        }
    },
    created() {
        this.getMyCourses();
    }
}
</script>