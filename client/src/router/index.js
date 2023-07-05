import { createRouter, createWebHistory } from 'vue-router'
import InstructorLive from '../components/InstructorLive.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/livesession/:sessionId',
      name: 'Live Session',
      component: InstructorLive
    },
  ]
})

export default router