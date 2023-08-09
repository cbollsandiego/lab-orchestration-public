<template>
  <div class="full-page">
    <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
    <div class="title-container">
      <h1 class="title">Create Lab</h1>
    </div>
    <div class="form-group">
      <div class="input-container">
        <label for="title" class="question-label"><b>Title:</b></label>
        <input type="text" v-model="title" v-if="!this.$route.params.labName" id="title" class="question-input title-input">
        <input type="text" v-model="title" v-if="this.$route.params.labName" id="title" class="question-input title-input" disabled>
      </div>
    </div>
    <div v-for="question in questions" :key="question.order_num" class="question">
      <div class="question-header">
        <div class="question-content">
      
          <span class="question-order">{{ question.order_num }}</span>
          <div class="btn-group-vertical">
            <button @click="moveUp(question.order_num)" class="btn btn-default">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-chevron-up"
                viewBox="0 0 16 16">
                <path fill-rule="evenodd"
                  d="M7.646 4.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1-.708.708L8 5.707l-5.646 5.647a.5.5 0 0 1-.708-.708l6-6z" />
              </svg>
            </button>
            <button @click="moveDown(question.order_num)" class="btn btn-default">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-chevron-down" viewBox="0 0 16 16">
                <path fill-rule="evenodd"
                  d="M1.646 4.646a.5.5 0 0 1 .708 0L8 10.293l5.646-5.647a.5.5 0 0 1 .708.708l-6 6a.5.5 0 0 1-.708 0l-6-6a.5.5 0 0 1 0-.708z" />
              </svg>
            </button>
          </div>
          <div class="question-textarea-container">
            <textarea v-model="question.title" class="question-input"></textarea>
            <div class="form-check form-switch">
              <span>Checkpoint?</span>
              <input type="checkbox" v-model="question.checkpoint" id="flexSwitchCheckDefault" class="form-check-input">
            </div>
          </div>
        </div>
        </div>
      <div class="delete-question-wrapper">
        <button @click="removeQuestion(question.order_num)" class="delete-question">Delete</button>
      </div>
    </div>
    <button type="button" class="add-question" @click="newQuestion">Add Question
      <b>+</b></button>
    <div class="save-container">
      <button @click="saveLab" class="save-lab-button">Save</button>
      <button @click="saveAndQuit" class="quit-button">Save & Quit</button>
    </div>
    <button @click="deleteLab" v-if="this.$route.params.labName" class="btn btn-danger btn-sm my-2"> Delete Lab</button>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue'
import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"
export default {
  data() {
    return {
      title: "",
      questions: [],
      alertMessage: "",
      alertSuccess: false,
      click: '',
    };
  },
  components: {
    alert: Alert
  },
  created() {
      if(!this.$route.params.labName) {
          this.questions.push({ order_num: 1, title: "", type: "Question", checkpoint: false });
      }
      else {
          this.getOldLab()
      }
  },
  methods: {
    newQuestion() {
      this.questions.push({
        order_num: this.questions.length + 1,
        title: "",
        type: "Question",
        checkpoint: false
      });
    },
    removeQuestion(questionNum) {
      this.questions = this.questions.filter(question => question.order_num !== questionNum);
      for (var i = 0; i < this.questions.length; i++) {
        this.questions[i].order_num = i + 1;
      }
    },
    moveUp(questionNum) {
      if (questionNum !== 1) {
        this.questions[questionNum - 1].order_num = questionNum - 1;
        this.questions[questionNum - 2].order_num = questionNum;
        this.sortQuestions();
      }
    },
    moveDown(questionNum) {
      if (questionNum !== this.questions.length) {
        this.questions[questionNum - 1].order_num = questionNum + 1;
        this.questions[questionNum].order_num = questionNum;
        this.sortQuestions();
      }
    },
    sortQuestions() {
      this.questions.sort((a, b) => a.order_num - b.order_num)
    },
    handleSubmit(question) {
      if (question) {
        this.questionForm = question.order_num
      };
      console.log(this.questionForm);
      const payload = {
        answer: this.questionForm,

      };
      //this.addAnswer(payload);
    },
    /*addAnswer(payload) {
      const path = `http://localhost:5001/${this.$route.params.course_name}/${this.$route.params.semester}/${this.$route.params.section}/${this.$route.params.session}/${this.$route.params.group}`;
      axios.post(path, payload)
        .then(() => {
          this.newQuestion();
          this.click = payload
        })
        .catch((error) => {

          console.log(error);
          this.newQuestion();

          //this.alertSuccess = false;
          //this.message='Error occurred when saving messsage'
          //this.showMessage = true;
        });

    },*/
    deleteLab() {
      this.removeLab();
    },
    removeLab() {
      const path = `http://localhost:5001/newlab/delete/${this.$route.params.labName}`;
      const accessToken = localStorage.getItem('token')
      axios.delete(path, {headers: {'Authorization': accessToken}})
        .then(() => {
          this.$router.push({ name: 'Lab List'})
        })
        .catch((error) => {
          console.error(error);
        });
    },
    saveLab() {
        if(!this.$route.params.labName) {
            this.submitNewLab()
        }
        else {
            this.submitEdit()
        }
    },
    saveAndQuit() {
        this.saveLab()
        this.$router.push({ name: 'Lab List'})
    },
    submitNewLab() {
      const newLab = { title: this.title.trim(), questions: this.questions, num_questions: this.questions.length };
      const path = 'http://localhost:5001/newlab/submit'
      axios.post(path, newLab)
        .then((response) => {
          if (response.data.status === 'failure') {
            this.alertMessage = "Failure creating lab. Something went wrong."
            this.alertSuccess = false
          }
          else if (response.data.status == "name exists") {
            this.alertMessage = "Failure creating lab. Make sure the lab name is unique and no questions are blank."
            this.alertSuccess = false
          }
          else {
            this.alertMessage = 'Lab successfully created!'
            this.alertSuccess = true
            this.questions = [{ order_num: 1, title: "", type: "Question", checkpoint: false }]
            this.title = ""
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },
    getOldLab() {
        const path = `http://localhost:5001/editlab/${this.$route.params.labName}/get`
        const accessToken = localStorage.getItem('token')
        axios.get(path, {headers: {'Authorization': accessToken}})
            .then((res) => {
                if(res.data.status === 'success') {
                    this.title = res.data.title;
                    this.questions = JSON.parse(res.data.questions)
                }
                else {
                    this.alertMessage = 'Failure fetching lab'
                    this.alertSuccess = false
                }
            })
            .catch((error) => {
              console.log(error)
            })
    },
    submitEdit() {
        const path = `http://localhost:5001/editlab/${this.$route.params.labName}/post`
        const accessToken = localStorage.getItem('token')
        const newLab = { questions: this.questions, num_questions: this.questions.length };
        axios.post(path, newLab, {headers: {'Authorization': accessToken}})
            .then((res) => {
                if(res.data.status === 'failure') {
                    this.alertMessage = 'Failure saving lab.'
                    this.alertSuccess = false
                }
                else {
                    this.alertMessage = 'Lab saved'
                    this.alertSuccess = true
                }
            })
            .catch((error) => {
                console.log(error)
            })
    }
  }
}
</script>
