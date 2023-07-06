import { createRouter, createWebHistory } from 'vue-router'
import InstructorLive from '../components/InstructorLive.vue'
import Login from '../components/Login.vue'

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
  ]
})

export default router