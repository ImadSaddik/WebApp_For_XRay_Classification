import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ActivateAccountView from '@/views/ActivateAccountView.vue'
import ResetPasswordView from '@/views/ResetPasswordView.vue'
import ResetPasswordConfirmationView from '@/views/ResetPasswordConfirmationView.vue'
import PredictView from '@/views/PredictView.vue'
import GalleryView from '@/views/GalleryView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LogInView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/activate/:uid/:token',
    name: 'activate',
    component: ActivateAccountView
  },
  {
    path: '/reset_password',
    name: 'reset_password',
    component: ResetPasswordView
  },
  {
    path: '/password/reset/confirm/:uid/:token',
    name: 'reset_password_confirm',
    component: ResetPasswordConfirmationView
  },
  {
    path: '/predict',
    name: 'predict',
    component: PredictView
  },
  {
    path: '/gallery',
    name: 'gallery',
    component: GalleryView
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
