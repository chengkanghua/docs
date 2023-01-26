import {createRouter, createWebHistory} from 'vue-router'
import Login from '../views/Login.vue'
import Base from '../views/Base'
import ShowCenter from '../views/ShowCenter'
import Host from '../views/Host'
import store from "../store"


const routes = [
    {

        path: '/uric',
        alias: '/', // 给当前路径起一个别名
        name: 'Base',
        component: Base, // 快捷键：Alt+Enter快速导包,
        children: [
            {
                meta: {
                    title: '展示中心',
                    authenticate: false,
                },

                path: 'show_center',
                alias: '', // 给当前路径起一个别名
                name: 'ShowCenter',
                component: ShowCenter
            },
            {
                meta: {
                    title: '主机管理',
                    authenticate: true,
                },
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


];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});


// 路由守卫，主要是编写一些在页面跳转过程中， 需要自动执行的代码。例如：修改页面头部标题，验证权限。
router.beforeEach((to, from, next) => {
    alert("页面跳转");
    document.title = to.meta.title;
    console.log("token:::", store.getters.token);
    if (to.meta.authenticate && (store.getters.token === '')) {
        // 如果访问需要登录的页面，但是没有token则默认跳转到login登陆页面
        next({name: 'Login'})
    } else {
        next()
    }
});

export default router

