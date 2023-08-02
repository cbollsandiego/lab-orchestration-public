<template>
  <div class="full-page">
    <alert :message="alertMessage" :isSuccess="alertSuccess"></alert>
    <div class="title-container">
      <h1 class="title">Create Lab</h1>
    </div>
    <div class="form-group">
      <div class="input-container">
        <label for="title" class="question-label"><b>Title:</b></label>
        <input type="text" v-model="title" id="title" class="question-input title-input">
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

    <button type="button" class="add-question" @click="handleSubmit(questions) && newQuestion">Add Question
      <b>+</b></button>
    <!--<alert :message="message" :isSuccess="alertSuccess" v-if="(newQuestion) == click && showMessage" @click="showMessage = false">
                </alert>-->
    <button @click="submitNewLab" class="create-lab-button">Create Lab</button>
    <button @click="deleteLab" class="btn btn-danger btn-sm my-2"> Delete Lab</button>
    
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
      //alertSuccess: true,
      //showMessage: false,
    };
  },
  components: {
    alert: Alert
  },
  created() {
    this.questions.push({ order_num: 1, title: "", type: "Question", checkpoint: false });
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
      this.addAnswer(payload);

    },
    addAnswer(payload) {
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
          // this.showMessage = true;
        });

        },
        deleteLab(){

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
    }
  },
};
</script>

<style>
.form-switch .form-check-input {
  height: 20px;
  width: 48px;
}

.form-switch .form-check-input:focus {
  border-color: rgba(0, 0, 0, 0.25);
  outline: 0;
  box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba(0,0,0,0.25)'/></svg>");
}

.form-switch .form-check-input:checked {
  background-color: #4caf50;
  border-color: #4caf50;
  border: none;
  background-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='-4 -4 8 8'%3e%3ccircle r='3' fill='rgba(255,255,255,1.0)'/></svg>");
}

html,
body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.full-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f2f2f2;
  padding: 20px;
}

.title-container {
  width: 800px;
  text-align: center;
  margin-bottom: 20px;
}

.title {
  margin: 0;
}

.form-group {
  margin-bottom: 15px;
  width: 800px;
}

.input-container {
  display: flex;
  align-items: center;
  width: 100%;
}

.question-label {
  flex-basis: 70px;
  font-weight: bold;
  margin-right: -12px;
}

.question {
  margin-bottom: 20px;
  position: relative;
}

.question-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 800px;
}

.question-content {
  display: flex;
  align-items: flex-start;
  width: 100%;
}

.question-order {
  flex-basis: 50px;
  font-weight: bold;
  font-size: 20px;
  margin-top: 34px;
}

.question-textarea-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.question-input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  height: 100px;
  resize: vertical;
  width: 100%;
}

.title-input {
  height: 32px;
  line-height: 32px;
}

.delete-question-wrapper {
  position: absolute;
  right: 0;
  bottom: -10px;
}

.delete-question {
  background-color: #ff0000;
  color: #fff;
  border: none;
  padding: 5px 8px;
  cursor: pointer;
  border-radius: 3px;
}

.add-question,
.create-lab-button {
  background-color: #4caf50;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}

.add-question {
  margin-bottom: 10px;
}

.create-lab-button {
  margin-bottom: auto;
  margin-top: 5px;
}

.question-order {
  flex-basis: 50px;
  font-weight: bold;
  font-size: 20px;
  margin-top: 34px;
  margin-right: -40px;
}

.btn-group-vertical {
  margin-top: 10px;
}</style>