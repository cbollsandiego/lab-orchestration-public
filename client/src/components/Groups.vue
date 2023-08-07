<template>
    <div class="full-page">
      <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
      <router-link 
        :to="{name: 'Course', params: 
        {course_name: this.$route.params.course_name, semester: this.$route.params.semester, section: this.$route.params.section}}" 
        class="Course back-button">
        <button type="button" class="btn btn-outline-secondary">Back to Course</button>
    </router-link>
      <h1>Groups for {{this.$route.params.course_name}} {{this.$route.params.session}}</h1>
      <div class="import-wrapper">
        <div class="import-text">Import from past lab:</div>
        <div class="import-controls">
          <select class="form-select" v-model="importSession">
            <option disabled value="">Select lab to import from</option>
            <option v-for="session in oldSessions" :key="session.name">
              {{ session.name }}
            </option>
          </select>
          <button class="import-button" @click="importGroups">Import</button>
        </div>
      </div>
      <div class="buttons-wrapper">
        <button class="new-button" @click="newGroup()">New Group</button>
        <button class="save-button" @click="postGroups">Save Groups</button>
        <button type="button" class="new-button" @click="randomize">Randomize Groups</button>
      </div>
      <div class="group-box">
        <div v-for="group in groups" class="group">
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
import { getTransitionRawChildren } from 'vue';
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
            showModal: false,
            alertMessage: '',
            alertSuccess: false
        }
    },
    created() {
        this.getGroups()
    },
    beforeUnmount() {
        this.postGroups()
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
                this.$router.push({ name: 'Login'})
            })
        },
        async importGroups() {
            if(!this.importSession) {
                this.alertMessage = "You must select a lab to import"
                this.alertSuccess = false
                return
            }
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.importSession}/getgroups`
            const accessToken = localStorage.getItem('token')
            await axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                this.groups = res.data.groups
                this.alertMessage = "Imported Successfully."
                this.alertSuccess = true
                this.postGroups()
            })
            .catch((error) => {
                console.log(error)
            })
            this.$router.go(0)
        },
        async postGroups() {
            this.checkNames()
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/postgroups`
            const accessToken = localStorage.getItem('token')
            const payload = {'groups': this.groups}
            await axios.post(path, payload, {headers: {'Authorization': accessToken}})
            .then((res) => {
                if(res.data.status === 'success') {
                    this.alertMessage = 'Updated Groups'
                    this.alertSuccess = true
                }
                else {
                    this.alertMessage = 'Failed to save groups'
                    this.alertSuccess = false
                }
            })
        },
        newGroup() {
            this.groups.push({name: '', members: []})
            this.checkNames()
        },
        checkNames() {
            let i = 1
            for(let group of this.groups) {
                if(group.name === '' || group.name.slice(0,5) === 'Group') {
                    group.name = 'Group' + ` ${i}`
                    i++
                }
            }
            i = 1
            for(let group of this.groups) {
                while(this.groups.filter(x =>x.name === group.name).length > 1) {
                    group.name = group.name + ` ${i}`
                    i++
                }
            }
        },
        removeGroup(groupName) {
            let g = this.groups.find(group => group.name === groupName)
            for(let i = 0; i < g.members.length; i++) {
                this.notInGroup.push(g.members[i])
            }
            this.groups = this.groups.filter(group => group.name != groupName)
        },
        randomize() {
            for(let group of this.groups) {
                for(let member of group.members) {
                    this.notInGroup.push(member)
                }
                group.members = []
            }
            this.shuffleNotInGroup();
            let i = 0
            while(this.notInGroup.length != 0) {
                this.groups[i%this.groups.length].members.push(this.notInGroup.shift())
                i++;
            }
        },
        shuffleNotInGroup() {
            for(var i = this.notInGroup.length -1; i > 0; i--) {
                var j = Math.floor(Math.random() * (i + 1));
                var temp = this.notInGroup[i];
                this.notInGroup[i] = this.notInGroup[j];
                this.notInGroup[j] = temp;
            }
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

.buttons-wrapper {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-bottom: 10px; 
  }

.import-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 10px;
    height: 100px;
    border: 2px solid #4caf50;
    border-radius: 10px;
    padding: 10px;
  }

.import-controls {
    display: flex;
    gap: 10px;
    height: 40px;
  }

.import-text {
    margin-bottom: 8px;
    font-weight: bold;
  }

.back-button {
    align-self: flex-start;
}
</style>