<template>
    <div class="container py-5">
      <h2 class="text-center mb-4">Session {{ $route.params.sessionId }}</h2>
      <div class="bg-light p-4">
        <groups-set :socket="socketio"></groups-set>
      </div>
    </div>
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
        this.socketio = io("127.0.0.1:5001");
        this.socketio.emit('enter_room', this.$route.params.sessionId);
    },
    components: {
        GroupsSet
    }
}
</script>

<style>
.container {
  background-color: #f8f9fa12;
  border-radius: 10px;
}

.bg-light {
  background-color: #ffffff;
}
</style>