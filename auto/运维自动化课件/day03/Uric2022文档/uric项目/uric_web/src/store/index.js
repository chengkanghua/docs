import {createStore} from 'vuex'


import createPersistedState from 'vuex-persistedstate'


export default createStore({
    state: {
        token: '',
        remember: false
    },
    plugins: [createPersistedState({ // setState,getState自动触发,防止刷新vuex清空，所以存到本地
        key: 'vuex',
        setState(key, state) {
            alert("token值", state.token);
            if (state.remember) {
                localStorage[key] = JSON.stringify(state)
            } else {
                sessionStorage[key] = JSON.stringify(state)
            }
        },
        getState(key, state) {
            if (sessionStorage.length === 0) {
                return {}
            }
            if (state.remember) {
                return JSON.parse(localStorage[key])
            } else {
                return JSON.parse(sessionStorage[key])
            }
        }
    })]
    ,
    getters: { // 类似静态方法
        token(state, getters) {
            // 获取token，先判断载荷是否有效，如果载荷是空对象，则没有token
            if (JSON.stringify(getters.payload) === '{}') {
                localStorage.removeItem('vuex');
                sessionStorage.removeItem('vuex');
                return ''
            } else {
                return state.token
            }
        },
        payload(state) {
            // 从token中获取载荷
            // 1. 从token中提取中间一段字符串
            let payloadArray = state.token.split('.')
            if (payloadArray.length < 1) {
                return {}
            }
            let payloadString = payloadArray[1]
            // 2. 通过json解析，把载荷转换成js对象
            let payload = null
            try {
                payload = JSON.parse(atob(payloadString))
            } catch (e) {
                return {}
            }
            // 3. 判断载荷中的有效期是否过期
            let nowTimeStamp = parseInt((new Date() - 0) / 1000)
            if (nowTimeStamp < payload.exp) {
                // 4. 如果没有过期，则直接返回载荷
                return payload
            }
            // 5. 如果过期，则清空token，返回空对象
            state.token = '';
            return {}
        }


    },
    mutations: {  // 类似methods
        setToken(state, token) {
            // 设置本地保存token
            state.token = token
        },
        setRemember(state, remember) {
            // 设置记住登陆状态
            // localStorage.removeItem('vuex');
            // sessionStorage.removeItem('vuex');
            state.remember = remember
        },


    },
    actions: {},
    modules: {}
})
