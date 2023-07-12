import { createRouter, createWebHistory } from 'vue-router'
import InstructorLive from '../components/InstructorLive.vue'
import Student_Lab from '../components/Student_Lab.vue'
import CreateLab from '../components/CreateLab.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/livesession/:sessionId',
      name: 'Live Session',
      component: InstructorLive
    },
    {
      path:'/:course_name/:semester/:section/:lab_num/:group/:session',
      name:'Student_Lab',
      component: Student_Lab
    },
    {
      path:'/create/lab',
      name: 'Create Lab',
      component: CreateLab

    }
  ]
})

export default router