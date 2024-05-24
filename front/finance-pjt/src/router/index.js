import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DepositView from '@/views/DepositView.vue'
import SavingsView from '@/views/SavingsView.vue'
import ExchangeView from '@/views/ExchangeView.vue'
import FindBankView from '@/views/FindBankView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import UserProfileView from '@/views/UserProfileView.vue'
import LoginView from '@/views/LoginView.vue'
import SigninView from '@/views/SigninView.vue'
import ItemDetail from '@/components/ItemDetail.vue'
import SavingDetail from '@/components/SavingDetail.vue'
import DepositQuiz from '@/components/DepositQuiz.vue'
import SavingsQuiz from '@/components/SavingsQuiz.vue'
import ArticleList from '@/components/ArticleList.vue'
import ArticleDetail from '@/components/ArticleDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/deposit',
      name: 'deposit',
      component: DepositView
    },
    {
      path: '/depositQuiz',
      name: 'depositQuiz',
      component: DepositQuiz
    },
    {
      path: '/savings',
      name: 'savings',
      component: SavingsView
    },
    {
      path: '/savingsQuiz',
      name: 'savingsQuiz',
      component: SavingsQuiz
    },
    {
      path: '/itemDetail/:itemPk',
      name: 'itemDetail',
      component: ItemDetail
    },
    {
      path: '/savingDetail/:itemPk',
      name: 'savingDetail',
      component: SavingDetail
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },
    {
      path: '/findBank',
      name: 'findBank',
      component: FindBankView
    },

    {
      path: '/articles',
      name: 'articles',
      component: ArticleView,
      children: [
        {
          path: 'articlelist',
          name: 'articlelist',
          component: ArticleList
        },
        { 
          path: ':articlePk', 
          name: 'articleDetail', 
          component: ArticleDetail
        },
      ]
    },
    {
      path: '/articleCreate',
      name: 'articleCreate',
      component: ArticleCreateView
    },
    {
      path: '/articleUpdate/:articlePk',
      name: 'articleUpdate',
      component: ArticleUpdateView
    },
    
    {
      path: '/profile/:username',
      name: 'profile',
      component: UserProfileView
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signin',
      name: 'signin',
      component: SigninView,
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    return { left: 0, top: 0 };
  }
})

export default router
