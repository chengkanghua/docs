import {createRouter, createWebHistory} from 'vue-router'
import Home from '../views/Home.vue'
import Article from '../components/Article.vue'
import Article2 from '../components/Article2.vue'
import Article3 from '../components/Article3.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },

    {
        path: '/article',
        name: 'Article',
        component: Article
    },

     {
        path: '/article/:year/:month',
        name: 'Article2',
        component: Article2
    },

    {
        path: '/articles',
        name: 'Article3',
        component: Article3
    },

];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router
