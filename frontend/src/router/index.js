import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/pages/index.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('@/pages/Analysis.vue'),
    meta: { title: '分析' }
  },
  {
    path: '/comments',
    name: 'Comments',
    component: () => import('@/pages/Comments.vue'),
    meta: { title: '评论' }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? to.meta.title + ' - 微博情感分析' : '微博情感分析系统'
  next()
})

export default router
