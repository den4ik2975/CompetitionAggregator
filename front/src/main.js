import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'
import App from './App.vue'

import Home from './pages/Home.vue'
import Favorites from './pages/Favorites.vue'
import Olympiad from '@/pages/Olympiad.vue'
import Participants from '@/pages/Participants.vue'
import User from '@/pages/User.vue'
import Notifications from '@/pages/Notifications.vue'

const app = createApp(App)

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/favorites', name: 'Favorites', component: Favorites },
  { path: '/notifications', name: 'Notifications', component: Notifications },
  { path: '/participants', name: 'Participants', component: Participants },
  { path: '/user', name: 'User', component: User },
  { path: '/olympiad', name: 'Olympiad', component: Olympiad },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

app.use(router)
app.use(autoAnimatePlugin)

app.mount('#app')