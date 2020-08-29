import Vue from 'vue'
import VueRouter from 'vue-router'
import JoinRoom from '../views/JoinRoom.vue'
import CreateRoom from '../views/CreateRoom.vue'
import About from '../views/About.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/joinroom'
  },
  {
    path: '/joinroom',
    name: 'JoinRoom',
    component: JoinRoom
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/createroom',
    name: 'CreateRoom',
    component: CreateRoom
  },
  {
    path: '*',
    redirect: '/joinroom'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
