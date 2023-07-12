<template>
  <div class="create-lab">
    <alert :message="alertMessage"></alert>
    <h1 class="title">Create Lab</h1>
    <div class="form-group">
      <label for="title">Title:</label>
      <input type="text" v-model="title" id="title">
    </div>
    <div v-for="question in questions" :key="question.order_num" class="question">
      <div class="question-header">
        <div class="question-content">
          <span class="question-order">{{ question.order_num }}</span>
          <textarea v-model="question.title" class="question-input"></textarea>
        </div>
        <div class="question-controls">
          <div class="question-control">
            <label for="checkpoint" class="checkpoint-label">Checkpoint?</label>
            <input type="checkbox" v-model="question.checkpoint" id="checkpoint" class="question-checkbox">
          </div>
          <div class="question-control">
            <button @click="removeQuestion(question.order_num)" class="delete-question">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <button @click="newQuestion" class="add-question">Add Question <b>+</b></button>
    <button @click="submitNewLab" class="create-lab-button">Create Lab</button>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue'
export default {
  data() {
    return {
      title: "",
      questions: [],
      alertMessage: ""
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
    submitNewLab() {
      const newLab = { title: this.title, questions: this.questions, num_questions: this.questions.length };
      const path = 'http://localhost:5001/newlab/submit'
      axios.post(path, newLab)
        .then((response) => {
          if(response.data.status === 'failure') {
            this.alertMessage = "Failure creating Lab. Make sure the lab name is unique and no questions are blank."
          }
          else {
            this.alertMessage = 'Lab successfully created!'
            this.questions = [{ order_num: 1, title: "", type: "Question", checkpoint: false }]
            this.title = ""
          }
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.create-lab {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f2f2f2;
  padding: 20px;
}


.title {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.question {
  margin-bottom: 10px;
}

.question-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 800px;
}

.question-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.question-controls {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.question-order {
  flex-basis: 50px;
  font-weight: bold;
  margin-right: 10px;
}

.question-input {
  flex-grow: 1;
  margin-right: 10px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
  height: 100px;
  resize: vertical;
  width: 100%;
}

.checkpoint-label {
  margin-right: 5px;
}

.question-checkbox {
  margin-right: 10px;
}

.delete-question {
  background-color: #ff0000;
  color: #fff;
  border: none;
  padding: 5px 10px;
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
  margin-top: auto;
}
</style>
