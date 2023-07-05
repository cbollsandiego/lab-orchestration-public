<template>
    <groups-set
        :socket="socketio">
    </groups-set>
</template>

<script>
import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"
import GroupsSet from './GroupsSet.vue'
export default {
    data() {
        return {
            socketio: undefined
        }
    },
    created() {
        this.socketio = io("127.0.0.1:5000");
        this.socketio.emit('enter_room', this.$route.params.sessionId);
    },
    components: {
        GroupsSet
    }
}
</script>