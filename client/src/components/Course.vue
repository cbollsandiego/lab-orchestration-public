<template>
    <div v-if="currentUserRole === 'admin' || currentUserRole === 'instructor'">
        <instructor-course></instructor-course>
    </div>
    <div v-if="currentUserRole === 'student' || currentUserRole === 'assistant'">
        <student-course></student-course>
    </div>
</template>

<script>
import axios from 'axios';
import InstructorCourse from './InstructorCourse.vue'
import StudentCourse from './StudentCourse.vue'
export default {
    data() {
        return {
            currentUserRole: ''
        }
    },
    components: {
        InstructorCourse,
        StudentCourse
    },
    created() {
        const path = 'http://localhost:5001/getuserid'
        const accessToken = localStorage.getItem('token')
        axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.currentUserRole = res.data.role
            })
            .catch((error) => {
                console.log(error)
                this.$router.push({ name: 'Login'})
            })
    }
}
</script>

