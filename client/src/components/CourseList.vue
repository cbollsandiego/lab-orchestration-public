<template>
    <div class="container">
        <table class="table table-striped table-bordered">
            <thead>

                <router-link :to="{ name: 'Create Course' }" class="route-link">
                    <button>
                        <a class="nav-link"> Create Course</a>
                    </button>
                </router-link>
                



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
                    <td>{{ course.id }}</td>
                    <td>
                        <router-link 
                        :to="{name: 'Course', params: 
                        {course_name: course.course_name, semester: course.semester, section: course.section_num}}" 
                        class="Course">
                        {{ course.course_name }}
                        </router-link>
                    </td>
                    <td>{{ course.semester }}</td>
                    <td>{{ course.section_num }}</td>
                    <td>{{ course.course_instructor }}</td>
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
            courses: []
        }
    },
    methods: {
        getCourses() {
            const path = 'http://localhost:5001/course_list';
            let accessToken = localStorage.getItem('token')
            console.log(accessToken)
            axios.get(path, { headers: { 'Authorization': accessToken, } })
                .then((res) => {
                    this.courses = res.data;
                })
                .catch((error) => {
                    console.error(error);
                    this.$router.push({ name: 'Login'})
                });
        }
    },
    created() {
        this.getCourses();
    }
}
</script>