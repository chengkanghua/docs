import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import settings from "@/settings";
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import 'xterm/css/xterm.css'
import 'xterm/lib/xterm'

const app = createApp(App);

app.use(store).use(router).use(Antd).mount('#app');

app.config.globalProperties.$settings = settings;


// 配置echarts插件
let echarts = require('echarts');
app.config.globalProperties.$echarts = echarts;

