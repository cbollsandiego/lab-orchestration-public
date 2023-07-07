import { createRouter, createWebHistory } from 'vue-router'
import InstructorLive from '../components/InstructorLive.vue'
import Login from '../components/Login.vue'
import Student_Lab from '../components/Student_Lab.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/livesession/:sessionId',
      name: 'Live Session',
      component: InstructorLive
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/:course_name/:semester/:section/:lab_num/:group/:session',
      name: 'Student_Lab',
      component: Student_Lab
    },
  ]
})

export default router