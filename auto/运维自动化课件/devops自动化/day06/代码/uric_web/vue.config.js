const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
     devServer: {
         host:"www.uric.cn",
         port: "8080",
     },
})
