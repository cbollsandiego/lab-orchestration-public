<template>
    <div class="full-page">
        <h1>{{this.name}}</h1>
        <h3>{{this.instructor}}</h3>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Lab Sessions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="group in groups">
                    <td>
                        <router-link 
                        :to="{name: 'Student_Lab', params: 
                        {course_name: $route.params.course_name, semester: $route.params.semester, section: $route.params.section, session: group.session, group: group.group}}"
                        >
                            {{group.session}} - {{group.group}}
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
import Alert from './Alert.vue'
export default {
    data() {
        return {
            groups: [],
            name: '',
            instructor: ''
        }
    },
    components: {
        alert: Alert
    },
    created() {
        this.getInfo()
    },
    methods: {
        getInfo() {
            const path = `http://localhost:5001/getcourse/student/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}`
            const accessToken = localStorage.getItem('token')
            axios.get(path, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    if(res.data.status === 'success') {
                        this.name = res.data.name
                        this.instructor = res.data.instructor
                        this.groups = res.data.groups
                    }
                    else {
                        this.$router.push({name: 'My Courses'})
                    }
                })
                .catch((error) => {
                    console.log(error)
                    this.$router.push({ name: 'Login'})
                })
            window.scrollTo(0,0)
        }
    }
}
</script>