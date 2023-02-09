const {defineConfig} = require('@vue/cli-service')

module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        // host: "localhost",
        /* 本地ip地址 */
        //host: "192.168.0.131",
        host: "www.uric.cn", //局域网和本地访问
        port: "8080",
        // hot: true,
        /* 自动打开浏览器 */
        // open: false,
        /*overlay: {
            warning: false,
            error: true
        },*/
        /* 跨域代理 */
        /*proxy: {
            "/api": {
                /!* 目标代理服务器地址 *!/
                target: "http://xxxx.top", //
                /!* 允许跨域 *!/
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    "^/api": ""
                }
            }
        }*/
    },
});