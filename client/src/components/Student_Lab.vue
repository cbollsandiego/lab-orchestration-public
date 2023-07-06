<template>
    <div class="container">
        <p>Lab {{ $route.params.lab_num }}</p>
        <input type="submit" value="Raise hand" onclick="return sendCommand('handup')">
    <input type="submit" value="Lower hand" onclick="return sendCommand('handdown')">
        <form>
            <div v-for="(question, index) in questions" :key="index" class="mb-3">
                <label for="addBookTitle" class="form-label">Question {{ question.order_num }}: {{ question.title }}</label>
                <textarea class="form-control" id="addBookTitle" placeholder="Question 1 "> Enter answer here!
            </textarea>
                <button type="button" class="btn btn-warning btn-sm">Submit</button>
                <div v-if="question.checkpoint">
                    <h4>
                        Check Point.
                    </h4>
                    <input type="radio" name="Si">Yes<br>
                    <input type="radio" name="Si">No<br>
                </div>
            </div>





        </form>
    </div>
</template>

<script>
import axios from 'axios';
import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"
export default {
    data() {
        return {
            questions: [],
            socket: undefined
        };
    },
    methods: {
        getQuestions() {
            const path = 'http://localhost:5001/comp110/sp23/1/2/2';
            axios.get(path)
                .then((res) => {
                    this.questions = res.data.questions;
                })
                .catch((error) => {
                   console.log("error");
                    console.error(error);
                });
        },
        sendCommand(command) {
            socket.emit('command_send', this.$route.params.group, command);
        }
    }, 
    created() {
        this.getQuestions();
        this.socket = io("127.0.0.1:5001");
        this.socket.emit("enter_room", this.$route.params.session);
    },
};
</script>
  