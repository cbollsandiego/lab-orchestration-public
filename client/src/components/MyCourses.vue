<template>
<h2>My Courses</h2>
<p>{{ courses_taught }}</p>
<div v-if="courses_taught.length >0">
    <p>Courses Taught</p>
    <ul>
        <li v-for="course in courses_taught">
            {{ course.course_name }}

        </li>
    </ul>
</div>
<div v-if="courses_in.length >0">
    <p>Courses In</p>
    <ul>
        <li v-for="course in courses_in">
            {{ course.course_name }}

        </li>
    </ul>
</div>
</template>

<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                courses_taught: [],
                courses_in: []
            };
        },
        methods: { 
            getMyCourses() {
                const path = 'http://localhost:5001/my_courses';
                axios.get(path)
                    .then((res) => {
                        this.courses_taught=res.data;
                        this.courses_in=[1];
                    })
                    .catch((error) => {
                        console.error(error);
                    });

            }
        },
        created() { 
            this.getMyCourses();
        }
    }
</script>