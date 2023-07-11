<template>
    <div>
        <h1>{{title}}</h1>
        Title: 
        <input type="text" v-model="title">
    </div>
    <div v-for="question in questions">
        {{question.order_num}}
        <input type="text" v-model="question.title">
        <input type="checkbox" v-model="question.checkpoint">
        <button @click="removeQuestion(question.order_num)">Delete Question</button>
    </div>

    <button @click="newQuestion">Add Question+</button>
    <button @click="submitNewLab">Create Lab</button>
</template>

<script>
export default {
    data() {
        return {
            title: "",
            questions: []
        }
    },
    created() {
        this.questions.push({'order_num':1, 'title': '', 'type': 'Question', 'checkpoint': false})
    },
    methods: {
        newQuestion() {
            this.questions.push({'order_num': this.questions.length + 1, 'title': '', 'type': 'Question', 'checkpoint': false})
        },
        removeQuestion(questionNum){
            this.questions = this.questions.filter(question => question.order_num != questionNum);
            for(var i=0; i < this.questions.length; i++) {
                this.questions[i].order_num = i+1;
            }
        },
        submitNewLab() {
            var newLab = {'title':this.title, 'questions': this.questions, 'num_questions': this.questions.length}
        }
    }
}
</script>