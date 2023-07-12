<template>
    <div class="container">
        <p>Lab {{ $route.params.lab_num }}</p>
        <div class="container">
            <div class="row">
                <div class="col-1 border border-primary border-3 rounded-circle " v-for="index in progress"
                    style="width:30px ; height: 30px; background-color: blue;">
                    1
                </div>
                <div class="col-1 border border-primary border-3 rounded-circle "
                    v-for="index in total_questions - progress" style="width:30px ; height: 30px; background-color: white">
                    1
                </div>
            </div>
        </div>
        <input type="submit" value="Raise hand" @click="sendCommand('handup')" style="color:blue">
        <input type="submit" value="Lower hand" @click="sendCommand('handdown')">
        <div v-for="(question, index) in questions" :key="index" :id="question.order_num" class="mb-3">
            <form v-if="parseInt(question.order_num) <= progress + 1">
                <label for="addAnswer" class="form-label">Question {{ question.order_num }}: {{ question.title }}</label>
                <textarea class="form-control" :id="question.order_num"
                    v-model="questionForm.answer[question.order_num]">
                    Enter answer here!
                </textarea>
                <button type="button" class="btn btn-warning btn-sm" @click="handleSubmit(question)">Submit</button>
                <alert :message="message" v-if="showMessage" ></alert>
                <div v-if="question.checkpoint">
                    <h4>
                        Check Point.
                    </h4>

                    <input type="radio" value="Yes" @click="sendCommand('')" name="Si" id="yes" checked="checked">Yes "<br>

                    <input type="radio" value="No" @click="sendCommand('')" name="Si" id="no" checked="checked">No<br>





                </div>
            </form>
        </div>
    </div>


    
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';
import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"
export default {
    data() {
        return {
            questions: [],
            progress: 0,
            total_questions: 0,
            socket: undefined,
            messsage:'',
            showMessage: false,
            questionForm: {
                id: '',
                answer: {},
            },

        };
    },
    components: {
        alert: Alert
        
    },


    methods: {
        getQuestions() {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.lab_num}/${this.$route.params.group}`;
            axios.get(path)
                .then((res) => {
                    this.questions = res.data.questions;
                    this.questionForm.answer = res.data.answers;
                    this.progress = res.data.progress;
                    this.total_questions = res.data.total_questions;

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
                    this.message = 'Answer saved';
                    this.showMessage = true;
                })
                .catch((error) => {

                    console.log(error);
                    this.getQuestions();
                    this.showMessage = true;
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
            // this.addAnswer='';
        },

    },
    created() {
        this.getQuestions();
        this.socket = io("127.0.0.1:5001");
        this.socket.emit("enter_room", this.$route.params.session);
    },
    //updateForm (input, value ) {
    // this.form[input]= value

    //}

    //  saving data after refresh
    //localStorage
    //sessionStorage
    //v-model
    //input.value = input.value.replace(); input.saveValue()
}
//};



</script>





