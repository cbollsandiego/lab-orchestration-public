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
            @scoreUpdated="updateGroups">
        </group-box>
    </div>
    `,
    async created() {
        const response = await fetch("http://127.0.0.1:5000/labs/fetch/" + this.$sessionId);
        const data = await response.json();
        for(var i = 0; i < data.length; i++) {
            data[i].score = 0;
        }
        this.groups = data
    },
    methods: {
        updateGroups(data) {
            console.log(data)
            var group = this.groups.find(group => {
                return group.group_id === data.groupId
            })
            console.log(group)
            group.score = data.score;
            console.log(group);
            console.log(this.groups);
            this.groups.sort((a, b) => b.score - a.score)
            console.log(this.groups)
        },
    },
}