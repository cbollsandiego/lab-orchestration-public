<template>
    <div class="container">
        <p>Lab {{ $route.params.lab_num }}</p>
        <div class="container">
  <div class="row" >
    <div class="col-1 border border-primary border-3 rounded-circle " v-for="index in 5" style="width:30px ; height: 30px; background-color: blue;">
      1
    </div>
    <div class="col-1 border border-primary border-3 rounded-circle " v-for="index in 5" style="width:30px ; height: 30px; background-color: white">
      1
    </div>
  </div>
</div>
        <input type="submit" value="Raise hand" @click="sendCommand('handup')">
        <input type="submit" value="Lower hand" @click="sendCommand('handdown')">
        <div v-for="(question, index) in questions" :key="index" :id="question.order_num" class="mb-3">
            <form>
                <label for="addAnswer" class="form-label">Question {{ question.order_num }}: {{ question.title }}</label>
                <textarea class="form-control" :id="question.order_num" v-model="questionForm.answer[question.order_num]">
                    Enter answer here!
                </textarea>
                <button type="button" class="btn btn-warning btn-sm" @click="handleSubmit(question)">Submit</button>
                <div v-if="question.checkpoint">
                    <h4>
                        Check Point.
                    </h4>

                    <input type="radio" value="First checkpoint" @click="sendCommand('At a checkpoint')" name="Si"
                        id="First Checkpoint" disabled="disabled" checked="checked">Yes<br>


                    <input type="radio" value="First checkpoint" @click="sendCommand('At a checkpoint')" name="Si"
                        id="First Checkpoint" disabled="disabled" checked="checked">...<br>



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
                id: '',
                answer: {},

            },
        };
    },
    methods: {
        getQuestions() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.lab_num}/${this.$route.params.group}`;
            axios.get(path)
                .then((res) => {
                    this.questions = res.data.questions;
                    this.answer = res.data.answers;
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
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.lab_num}/${this.$route.params.group}`;
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
                this.questionForm.id = question.order_num

            };
            console.log(this.questionForm.answer);
            const payload = {
                answer: this.questionForm.answer,
                id: this.questionForm.id,
            };
            this.addAnswer(payload);

        },
        initForm() {
            this.questionForm.answer = {};
            this.questionForm.id = '';
        },

    },
    created() {
        this.getQuestions();
        this.socket = io("127.0.0.1:5001");
        this.socket.emit("enter_room", this.$route.params.session);
    },
    EnableDisableTextbox() {


        // EnableDisableTextBox() {
        // if ($(''))
        // this.get...("...).display = display.hidden;




        //}



    }
};



</script>

<!--progress  bar?-->



