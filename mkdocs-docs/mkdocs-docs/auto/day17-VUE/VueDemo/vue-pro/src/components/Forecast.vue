<template>
    <h1>天气预报</h1>
    <p><input type="text" placeholder="请输入查询城市" v-model="choose_city">
        <button @click="sendAjax">查询</button>
    </p>

    <table border="1" v-if="forecasts.length>1">
        <tr>
            <td>日期</td>
            <td>类型</td>
            <td>最高气温</td>
            <td>最低气温</td>
            <td>风向</td>
        </tr>

        <tr v-for="day_forecast in forecasts">
            <td>{{day_forecast.date}}</td>
            <td>{{day_forecast.type}}</td>
            <td>{{day_forecast.high}}</td>
            <td>{{day_forecast.low}}</td>
            <td>{{day_forecast.fengxiang}}</td>
        </tr>
    </table>
</template>

<script>
    import http from "axios";

    export default {
        name: "Forecast",
        data() {
            return {
                forecasts: [],
                // choose_city: "北京"
            }
        },
        methods: {
            sendAjax() {
                var that = this;

                http.get("http://wthrcdn.etouch.cn/weather_mini", {
                    params: {
                        city: that.choose_city,
                    }
                }).then(function (response) {
                    console.log("response", response);

                    that.forecasts = response.data.data.forecast
                })
            },
        },

        created() {
            this.sendAjax()
        },
        watch: {
            choose_city(newVal, oldVal) {
                this.sendAjax()
            },
        },
        props: {  // 接收来自父组件的数据
            choose_city: {
                default: "北京",
                type: String,
            }
        },
    }
</script>

<style scoped>

    tr td {
        padding: 10px;
        width: 100px;
    }

    table {
        margin: 0 auto;
    }

</style>