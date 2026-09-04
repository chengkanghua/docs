import {createRouter, createWebHistory} from 'vue-router'
import ShowCenter from '../views/ShowCenter.vue'
import Login from '../views/Login.vue'
import Base from '../views/Base'
import Host from '../views/Host'
import Console from '../views/Console'
import MultiExec from '../views/MultiExec'
import store from "../store"

const routes = [
    {
        path: '/uric',
        alias: '/', // 给当前路径起一个别名
        name: 'Base',
        component: Base, // 快捷键：Alt+Enter快速导包
        children: [
            {
                meta: {
                    title: '展示中心',
                    authenticate: false,
                },
                path: 'show_center',
                alias: '',
                name: 'ShowCenter',
                component: ShowCenter
            },
            {
                meta: {
                    title: '资产管理',
                    authenticate: true,
                },
                path: 'host',
                name: 'Host',
                component: Host
            },
            {
                meta: {
                    title: 'Console',
                    authenticate: true,
                },
                path: 'console/:host_id',
                name: 'Console',
                component: Console
            },
            {
                path: 'multi_exec',
                name: 'MultiExec',
                component: MultiExec,
            }
        ]
    },


    {
        meta: {
            title: '账户登陆',
            authenticate: false,
        },
        path: '/login',
        name: 'Login',
        component: Login // 快捷键：Alt+Enter快速导包
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    document.title = to.meta.title;
    // console.log("to", to)
    // console.log("from", from)
    // console.log("store.getters.token:", store.getters.token)
    if (to.meta.authenticate && store.getters.token === "") {
        next({name: "Login"})
    } else {
        next()
    }
});

export default router

