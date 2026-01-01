import { createWebHistory, createRouter } from 'vue-router'

import Index from '../pages/Index.vue'
import NotFound from '../pages/NotFound.vue'

const routes = [
  { path: '/', component: Index },
  { path: '/:pathMatch(.*)*', component: NotFound },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
