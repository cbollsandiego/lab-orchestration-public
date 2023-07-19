<template>
    <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
    <button @click="postGroups">Save Groups</button>
    <div v-for="group in groups">
        <input type="text" v-model="group.name" @change="checkNames">
        <draggable 
            class="list-group"
            v-model="group.members" 
            group="groups"
        >
            <template #item="{element}">
                <div class="list-group-item">{{element.name}}</div>
            </template>
        </draggable>
        <div v-for="member in group.members">
            {{ member.name }} {{ member.id }}
        </div>
    </div>
    <button @click="newGroup()">New Group</button>
    <select class="form-select" v-model="importSession">
        <option v-for="session in oldSessions">
            {{ session.name }}
        </option>
    </select>
    <button @click="importGroups">Import Groups</button>
    <h5>Not in Group:</h5>
    <div v-for="member in notInGroup">
        {{ member.name }} {{ member.id }}
    </div>
</template>

<script>
import axios from 'axios';
import draggable from 'vuedraggable'
import Alert from './Alert.vue'
export default{
    components: {
        alert: Alert,
        draggable
    },
    data(){
        return{
            groups:[],
            oldSessions:[],
            notInGroup: [],
            importSession: undefined,
            alertMessage: '',
            alertSuccess: false
        }
    },
    created() {
        this.getGroups()
    },
    methods: {
        getGroups() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/getgroups`
            const accessToken = localStorage.getItem('token')
            axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.groups = res.data.groups
                this.oldSessions = res.data.old_sessions
                this.notInGroup = res.data.not_in_group
            })
            .catch((error) => {
                console.log(error)
            })
        },
        async importGroups() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.importSession}/getgroups`
            const accessToken = localStorage.getItem('token')
            await axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.groups = res.data.groups
            })
            .catch((error) => {
                console.log(error)
            })
            this.postGroups()
        },
        postGroups() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/postgroups`
            const accessToken = localStorage.getItem('token')
            const payload = {'groups': this.groups}
            axios.post(path, payload, {headers: {'Authorization': accessToken}})
            .then((res) => {
                if(res.data.status === 'success') {
                    this.alertMessage = 'Updated Groups'
                    this.alertSuccess = true
                }
                else {
                    this.alertMessage = 'Failed to save groups'
                }
            })
        },
        newGroup() {
            this.groups.push({name: '', members: []})
        },
        checkNames() {
            for(let group of this.groups) {
                if(this.groups.filter(x => x.name === group.name).length > 1) {
                    group.name = group.name + '(1)'
                }
            }
        }
    }
}

</script>