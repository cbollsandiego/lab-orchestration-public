<template>
<div v-for="group in groups">
{{ group.name }}
<div v-for="member in group.members">
{{ member }}
</div>
</div>
<select class="form-select">
    <option v-for="session in old_sessions">
    {{ session.name }}
    </option>
</select>
</template>

<script>
import axios from 'axios';
export default{
        data(){
            return{
                groups:[],
                old_sessions:[],
            }
        },
        created() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/getgroups`
            let accessToken = localStorage.getItem('token')
            axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.groups = res.data.groups
                this.old_sessions = res.data.old_sessions
            })
            .catch((error) => {
                console.log(error)
            })
        }
}

</script>