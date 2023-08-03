<template >
     <div class="full-page">
   <div class=" container sticky-top lab-header my-3">
        <div class="container">
            <div class="row mb-2 ">
                <h3 class=" col text-start" style="font-family: Verdana, Geneva, Tahoma, sans-serif;">Lab {{
                    $route.params.session}}</h3>
                <div class="col-1 border border-white  border-3 rounded-circle " v-for="index in progress"
                    style="width:30px ; height: 30px; background-color: green;">

                </div>
                <div class="col-1 border border-li border-3 rounded-circle "
                    v-for="index in total_questions - progress" style="width:30px ; height: 30px; background-color: white">
                    
                </div>
            </div>
        </div>
        <input  class="btn btn-info" type="submit" value="Raise hand ✋ " v-if="!handup" @click="sendCommand('handup'); hand_raised('hand_raised')">
        <input  class="btn btn-info" type="submit" value="Lower hand" v-if="handup" @click="sendCommand('handdown'); hand_raised('hand_lowered')">
    </div>
    <div class="container ">
        <div v-for="(question, index) in questions" :key="index" :id="question.order_num" class="mb-4">
            <form v-if="parseInt(question.order_num) <= progress + 1">
                <label for="addAnswer" class="form-label">Question {{ question.order_num }}: {{ question.title }}</label>
                <textarea class="form-control" :id="question.order_num" v-model="questionForm.answer[question.order_num]">
                    Enter answer here!
                </textarea>
                <button type="button" class="btn btn-success btn-sm my-2"
                    @click="handleSubmit(question)">Submit</button>
                <alert :message="message" :isSuccess="alertSuccess" v-if="(question.order_num) == click && showMessage" @click="showMessage = false">
                </alert>
                <div style="font-family: Verdana, Geneva, Tahoma, sans-serif;color: rgb(255, 68, 51); margin-top: 7px;"
                    v-if="question.checkpoint">
                    <h5>
                        Checkpoint 
                    </h5>
                
                    <input class="" type="radio" value="Yes" @click="sendCommand('checkon')" name="Si" id="yes"
                        checked="checked">Yes <br>
                    <input class="" type="radio" value="No" @click="sendCommand('checkoff')" name="Si" id="no"
                        checked="checked">No<br>




                    
                </div>
            </form>
        </div>
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
            messsage: '',
            alertSuccess: true,
            click: '',
            handup: false,
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
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/${this.$route.params.group}`;
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
            this.socket.emit('command_send', this.$route.params.course_name, this.$route.params.session, this.$route.params.group, command);

        },
        addAnswer(payload) {
            const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/${this.$route.params.group}`;
            axios.post(path, payload)
                .then(() => {
                    this.getQuestions();
                    this.message = 'Answer saved';
                    this.alertSuccess= true;
                    this.showMessage = true;
                    this.click = payload.id
                })
                .catch((error) => {

                    console.log(error);
                    this.getQuestions();
                    this.alertSuccess= false;
                    this.message='Error occurred when saving messsage'
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

        },
        hand_raised(button_clicked) {
            if (button_clicked == "hand_raised") {
                this.handup = true;
            }
            else {
                this.handup = false;
            }
        }


    },
    created() {
        this.getQuestions();
        this.socket = io("127.0.0.1:5001");
        const roomName = this.$route.params.course_name + ' ' + this.$route.params.session;
        this.socket.emit("enter_room", roomName);
    },

}
</script>
<style scoped>
  .create-course-button {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
  }

  html, body {
    height: 100%;
    margin: 0;
    padding: 0;
  }

  .lab-header{
    background-color: #f2f2f2;
  }
  
  .full-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f2f2f2;
    padding: 20px;
  }

  .input-text-box {
    padding: 10px;
    width: 740px;
  }
</style>




