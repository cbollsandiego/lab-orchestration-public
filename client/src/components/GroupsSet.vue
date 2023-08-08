<template>
    <div class="container">
      <div class="row">
        <div class="col">
          <div class="row row-cols-1 row-cols-md-3 g-4">
            <div class="col" v-for="group in groups" :key="group.group_id">
              <div class="card h-100">
                <div class="card-body">
                  <GroupInfo
                    :name="group.name"
                    :members="group.members"
                    :groupId="group.group_id"
                    :score="group.score"
                    :handRaised="group.handRaised"
                    :atCheckpoint="group.atCheckpoint"
                    :progress="group.progress"
                    :maxProgress="group.maxProgress"
                    @instructorCommand="sendInstructorCommand"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import GroupInfo from './GroupInfo.vue'
import axios from 'axios'
export default {
    name: 'GroupsSet',
    props: {
        socket: {default: 1}
    },
    components: {
        GroupInfo
    },
    data() {
        return {
            groups: []
        }
    },
    async created() {
        var data;
        axios.get("http://127.0.0.1:5001/labs/fetch/" +this.$route.params.course_name+"/"+this.$route.params.semester+"/"+this.$route.params.section+ "/"+this.$route.params.session)
            .then((res) => {
                data = res.data;
                for(var i = 0; i < data.length; i++) {
                    data[i].score = 0;
                }
                this.groups = data
                this.calcScores()
            })
            .catch((error) => {
                console.log(error)
            });
    },
    mounted() {
        this.socket.on('command', (groupName, command) => {
            var group = this.groups.find(group => group.name == groupName)
            switch(command) {
                case 'handup': group.handRaised = true; break;
                case 'handdown': group.handRaised = false; break;
                case 'checkon': group.atCheckpoint = true; break;
                case 'checkoff': group.atCheckpoint = false; break;
            };
            var value = 0;
            group.handRaised ? value+=2 : value += 0;
            group.atCheckpoint ? value+=1 :  value += 0;
            group.score = value;
            this.sortGroups();
        });
        this.socket.on('progress_update', (groupName, questionNum) => {
          var group = this.groups.find(group => group.name == groupName)
          group.progress = questionNum
          this.sortGroups();
        })
    },
    methods: {
        sortGroups() {
            this.groups.sort((a, b) => b.score - a.score || a.progress - b.progress)
        },
        calcScores() {
          for(let group of this.groups) {
            var value = 0;
            group.handRaised ? value+=2 : value += 0;
            group.atCheckpoint ? value+=1 :  value += 0;
            group.score = value;
          }
          this.sortGroups();
        },
        sendInstructorCommand(command, groupName) {
            var group = this.groups.find(group => group.name == groupName)
            if(command === 'handoff') {
              group.handRaised = false;
            }
            if(command === 'checkoff') {
              group.atCheckpoint = false;
            }
            this.socket.emit('instructor_command', this.$route.params.course_name, this.$route.params.session, groupName, command);
            this.sortGroups();
        }
    }
}
</script>
