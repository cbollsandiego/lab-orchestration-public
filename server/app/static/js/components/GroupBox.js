export default {
    data() {
        return {
            handRaised: false,
            atCheckpoint: false,
            progress: 0,
        }
    },
    emits: ["scoreUpdated"],
    props: {
        name: {
            type: String
        },
        members: {
            type: Array
        },
        maxProgress: {
            type: Number,
            default: 0
        },
        groupId: {
            type: Number
        },
        score: {
            type: Number,
            default: 0
        },
    },
    template: `
        <h3>{{ name }} ({{groupId}})</h3>
        <div v-for="member in members">
            <p>{{ member }}</p>
        </div>
        <p v-show="handRaised">
            <i>Hand Raised</i>
        </p>
        <p v-show="atCheckpoint">
            <i>At checkpont!</i>
        </p>
        <p>
            <b>{{ progress }}/{{ maxProgress }}</b>
        </p>
    `,
    created() {
        console.log('created' + this.groupId);
        this.registerListener();
    },
    updated() {
        console.log('updated' + this.groupId);
        this.registerListener();
        //TODO: I think that this issue is that the socket listeners are registered in the component, but then they stay
        //with the old component when the array sorts and updates. That is why it works for the first hand raise, but then as
        //soon as the array is sorted differently it will stay in the same GroupBox component, but the GroupBox has all new values
        //Will work on fixing soon.
    },
    beforeUpdate() {
        console.log('beforeUpdate' + this.groupId);
        this.$socket.removeListener('command-'+this.groupId);
    },
    methods: {
        registerListener() {
            console.log('registering' + this.groupId);
            this.$socket.on('command-' + this.groupId, (command) => {
                console.log(this.groupId)
                console.log(this.name)
                switch(command) {
                    case 'handup': this.handRaised = true; break;
                    case 'handdown': this.handRaised = false; break;
                    case 'checkon': this.atCheckpoint = true; break;
                    case 'checkoff': this.atCheckpoint = false; break;
                };
                var value = 0;
                this.handRaised ? value+=2 : value += 0;
                this.atCheckpoint ? value++ :  value += 0;
                var returner = {'groupId': this.groupId, 'score': value}
                this.$emit('scoreUpdated', returner);
            });
        }
    },
}