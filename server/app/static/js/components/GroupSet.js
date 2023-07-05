import GroupBox from './GroupBox.js'
export default {
    components: {
        GroupBox
    },
    data() {
        return {
            groups: []
        }
    },
    template: `
    <div v-for="group in groups">
        <group-box 
            :name="group.name" 
            :members="group.members" 
            :groupId="group.group_id" 
            :score="group.score"
            :handRaised="group.handRaised"
            :atCheckpoint="group.atCheckpoint"
            :progress="group.progress"
            @scoreUpdated="updateGroups">
        </group-box>
    </div>
    `,
    async created() {
        const response = await fetch("http://127.0.0.1:5000/labs/fetch/" + this.$sessionId);
        const data = await response.json();
        for(var i = 0; i < data.length; i++) {
            data[i].score = 0;
            data[i].handRaised = false;
            data[i].atCheckpoint = false;
            data[i].progress = 0;
        }
        this.groups = data
    },
    mounted () {
        this.$socket.on('command', (groupId, command) => {
            console.log(groupId + command)
            var group = this.groups.find(group => group.group_id == groupId)
            switch(command) {
                case 'handup': group.handRaised = true; break;
                case 'handdown': group.handRaised = false; break;
                case 'checkon': group.atCheckpoint = true; break;
                case 'checkoff': group.atCheckpoint = false; break;
            };
            var value = 0;
            group.handRaised ? value+=2 : value += 0;
            group.atCheckpoint ? value++ :  value += 0;
            group.score = value;
            this.updateGroups();
        });
    },
    methods: {
        updateGroups() {
            this.groups.sort((a, b) => b.score - a.score)
        },
    },
}