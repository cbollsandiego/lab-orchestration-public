<template>
    <div class="full-page">
      <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
      <button class="save-button" @click="postGroups">Save Groups</button>
      <select class="form-select" v-model="importSession">
        <option v-for="session in oldSessions" :key="session.name">
          {{ session.name }}
        </option>
      </select>
      <button class="import-button" @click="importGroups">Import Groups</button>
      <br>
      <button class="new-button" @click="newGroup()">New Group</button>
      <div class="group-box">
        <div v-for="group in groups" :key="group.name" class="group">
          <h5>Group Name:</h5>
          <input type="text" v-model="group.name" @change="checkNames" class="name-input">
          <draggable class="list-group" v-model="group.members" group="groups" itemKey="group.members.id">
            <template #item="{ element }">
              <div class="list-group-item">{{ element.name }}</div>
            </template>
          </draggable>
          <button class="remove-button" @click="removeGroup(group.name)">Remove</button>
        </div>
        <div class="group">
            <h5>Not in Group:</h5>
            <draggable class="list-group" v-model="notInGroup" group="groups" itemKey="notInGroup.id">
            <template #item="{ element }">
                <div class="list-group-item">{{ element.name }}</div>
            </template>
            </draggable>
        </div>
      </div>
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
        },
        removeGroup(groupName) {
            let g = this.groups.find(group => group.name === groupName)
            for(let i =0; i < g.members.length; i++) {
                this.notInGroup.push(g.members[i])
            }
            this.groups = this.groups.filter(group => group.name != groupName)
        }
    }
}

</script>

<style>
.full-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f2f2f2;
    padding: 20px;
  }

.new-button,
.import-button,
.save-button  {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
  }

.remove-button {
    background-color: #ff0000;
    color: #fff;
    border: none;
    padding: 6px 10px;
    cursor: pointer;
    border-radius: 5px;
    margin-top: 6px;
}
.group-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
.group {
    margin: 10px;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
  }

.name-input {
    margin-bottom: 10px;
}

.list-group-item {
    cursor: grab;
  }
</style>