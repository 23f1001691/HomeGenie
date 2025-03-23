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
  {
    path: '/customer/:userID',
    name: 'CustomerDashboard',
    component: () => import('../views/CustomerDashboard.vue'),
    props: true
  },
  {
    path: '/book-services/:userID',
    name: 'BookServices',
    component: () => import('../views/BookServices.vue'),
    props: true
  },
  {
    path: '/customer-requests/:userID',
    name: 'CustomerRequests',
    component: () => import('../views/CustomerRequests.vue'),
    props: true
  },
  {
    path: '/professional/:userID',
    name: 'ProfessionalDashboard',
    component: () => import('../views/ProfessionalDashboard.vue'),
    props: true
  },
  {
    path: '/professional-history/:userID',
    name: 'ProfessionalHistory',
    component: () => import('../views/ProfessionalHistory.vue'),
    props: true
  },
  {
    path: '/professional-stats/:userID',
    name: 'ProfessionalStats',
    component: () => import('../views/ProfessionalStats.vue'),
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
