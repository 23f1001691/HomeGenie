import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sign-in',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/create-account',
    name: 'Signup',
    component: () => import('../views/Signup.vue')
  },
  {
    path: '/user-signup',
    name: 'CustomerSignup',
    component: () => import('../views/CustomerSignup.vue')
  },
  {
    path: '/work-signup',
    name: 'ProfessionalSignup',
    component: () => import('../views/ProfessionalSignup.vue')
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/AdminDashboard.vue')
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/Users.vue')
  },
  {
    path: '/services',
    name: 'Services',
    component: () => import('../views/Services.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
