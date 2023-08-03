<template>
    <div class="full-page">
      <div class="container py-5">
        <h2 class="text-center mb-4">Session {{ $route.params.session}}</h2>
        <div class="bg-light p-4">
          <groups-set :socket="socketio"></groups-set>
        </div>
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
        const roomName = this.$route.params.course_name + ' ' + this.$route.params.session;
        this.socketio.emit("enter_room", roomName);
    },
    components: {
        GroupsSet
    }
}
</script>
