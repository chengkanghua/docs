import {createRouter, createWebHistory} from 'vue-router'
import Login from '../views/Login.vue'
import Base from '../views/Base'
import ShowCenter from '../views/ShowCenter'
import Host from '../views/Host'


const routes = [
    {
        meta: {
            title: 'uric自动化运维平台'
        },
        path: '/uric',
        // alias: '/', // 给当前路径起一个别名
        name: 'Base',
        component: Base, // 快捷键：Alt+Enter快速导包,
        children: [
            {
                path: 'show_center',
                name: 'ShowCenter',
                component: ShowCenter
            },
            {
                path: 'host',
                name: 'Host',
                component: Host
            },
        ],
    },
    {
        meta: {
            title: '账户登陆'
        },
        path: '/login',
        name: 'Login',
        component: Login // 快捷键：Alt+Enter快速导包
    },

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router

