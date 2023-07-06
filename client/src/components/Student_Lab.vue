<template>
    <div class="container">
        <p>Lab {{ $route.params.lab_num }}</p>
        <input type="submit" value="Raise hand" @click="sendCommand('handup')">
        <input type="submit" value="Lower hand" @click="sendCommand('handdown')">
        <div v-for="(question, index) in questions" :key="index" :id="question.order_num" class="mb-3">
            <form>
                <label for="addAnswer" class="form-label">Question {{ question.order_num }}: {{ question.title }}</label>
                <textarea class="form-control" :id="question.order_num" v-model="questionForm.answer"> 
                    Enter answer here!
                </textarea>
                <button type="button" class="btn btn-warning btn-sm" @click="handleSubmit(question)">Submit</button>
                <div v-if="question.checkpoint">
                    <h4>
                        Check Point.
                    </h4>
                    <input type="radio" name="Si">Yes<br>
                    <input type="radio" name="Si">No<br>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"
export default {
    data() {
        return {
            questions: [],
            socket: undefined,
            questionForm: {
                id:'',
                answer: '',
      
            },
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
            this.socket.emit('command_send', this.$route.params.group, command);
        },
        addAnswer(payload) {
            const path = 'http://localhost:5001/comp110/sp23/1/2/2';
            axios.post(path, payload)
              .then(() => {
                  this.getQuestions();
                })
                .catch((error) => {

                    console.log(error);
                    this.getQuestions();
                });
        },
        handleSubmit(question) {
            if (question) {
                this.questionForm.id= question.order_num 
            };
            const payload = {
                answer: this.questionForm.answer,
                id: this.questionForm.id,
            };
            this.addAnswer(payload);
            this.initForm();
        },
        initForm() {
            this.questionForm.answer = '';
            this.questionForm.id ='';
        },

    }, 
    created() {
        this.getQuestions();
        this.socket = io("127.0.0.1:5001");
        this.socket.emit("enter_room", this.$route.params.session);
    },
};
</script>
  