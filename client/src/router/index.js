import { createRouter, createWebHistory } from 'vue-router'
import InstructorLive from '../components/InstructorLive.vue'
import Login from '../components/Login.vue'
import Student_Lab from '../components/Student_Lab.vue'
import CreateLab from '../components/CreateLab.vue'
import UserList from '../components/UserList.vue'
import CourseList from '../components/CourseList.vue'
import MyCourses from '../components/MyCourses.vue'
import CreateCourse from '../components/CreateCourse.vue'
import CreateUser from '../components/CreateUser.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/:course_name/:semester/:section/:session/livesession',
      name: 'Live Session',
      component: InstructorLive
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/:course_name/:semester/:section/:session/:group',
      name: 'Student_Lab',
      component: Student_Lab
    },
    {
      path: '/courselist',
      name: 'Course List',
      component: CourseList
    },
    {
      path: '/lab/create',
      name: 'Lab Create',
      component: CreateLab
    },
    {
      path: '/userlist',
      name: 'User List',
      component: UserList
    },
    {
      path: '/mycourses',
      name: 'My Courses',
      component: MyCourses
    },
    {
      path: '/course/create',
      name: 'Course Create',
      component: CreateCourse
    },
    {
      path: '/createuser',
      name: 'Course User',
      component: CreateUser

    }
  ]
})

export default router