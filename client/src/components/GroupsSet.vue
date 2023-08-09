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
                    :clock="group.clock"
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
                    data[i].clock = false;
                }
                this.groups = data
                this.checkTime()
                this.sortGroups()
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
            this.sortGroups();
        });
        this.socket.on('progress_update', (groupName, questionNum) => {
            var group = this.groups.find(group => group.name == groupName)
            group.progress = questionNum
            group.latestTime = new Date().toString().substring(16,24)
            group.clock = false
            this.sortGroups();
        });
        setInterval(() => {
            this.checkTime()
            this.sortGroups()
        }, 30*1000)
    },
    methods: {
        sortGroups() {
            this.calcScores()
            this.groups.sort((a, b) => b.score - a.score || a.progress - b.progress || a.latestTime - b.latestTime)
        },
        calcScores() {
          for(let group of this.groups) {
            var value = 0;
            group.handRaised ? value+=4 : value += 0;
            group.atCheckpoint ? value+=2 :  value += 0;
            group.clock ? value+=1 : value += 0;
            group.score = value;
          }
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
        },
        checkTime() {
            const time = new Date(new Date().getTime() - 4*60000).toString().substring(16, 24)
            for(let group of this.groups) {
                if(group.latestTime < time) {
                    group.clock = true
                }
                else {
                    group.clock = false
                }
            }
            this.sortGroups()
        }
    }
}
</script>
