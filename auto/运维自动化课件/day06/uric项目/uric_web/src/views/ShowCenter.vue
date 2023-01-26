<template>
    <h3>展示中心</h3>
    <a-row>
        <a-col :span="8">
            <p>
                <a-input-search
                        v-model:value="city"
                        placeholder="city"
                        enter-button="Search"
                        size="large"
                        @search="get_weather"
                />
            </p>

        </a-col>
    </a-row>

    <a-row>
        <a-col :span="16">
            <a-table :columns="columns" :data-source="data">
                <template #bodyCell="{ column, text }">
                    <template v-if="column.dataIndex === 'name'">
                        <a>{{ text }}</a>
                    </template>
                </template>
            </a-table>
        </a-col>
    </a-row>


    <a-row>
        <a-col :span="12">
            <div class="chart" ref="chart01"></div>
        </a-col>

        <a-col :span="12">
            <div class="chart" ref="chart02"></div>

        </a-col>
    </a-row>


</template>

<script>
    import axios from "axios"
    import * as echarts from 'echarts';
    import {ref} from 'vue';


    export default {
        name: "ShowCenter",
        setup() {
            const value = ref();

            return {
                value,
            };
        },
        data() {
            return {
                weather_list: [],
                city: "北京",
                columns: [
                    {
                        title: 'Date',
                        dataIndex: 'date',
                        key: 'date',
                    },
                    {
                        title: 'Type',
                        dataIndex: 'type',
                        key: 'type',
                        width: 80,
                    },
                    {
                        title: 'High',
                        dataIndex: 'high',
                        key: 'high 1',
                        ellipsis: true,
                    },
                    {
                        title: 'Low',
                        dataIndex: 'low',
                        key: 'low 2',
                        ellipsis: true,
                    },
                    {
                        title: 'FengXiang',
                        dataIndex: 'fengxiang',
                        key: 'fengxiang 3',
                        ellipsis: true,
                    },
                ],
                data: [],
            }
        },
        methods: {
            get_weather() {
                console.log("showCenter token:::",this.$store.getters.token)


                console.log(this.$settings.host);
                axios.get("http://wthrcdn.etouch.cn/weather_mini",
                    {
                        params: {
                            city: this.city
                        }
                    },
                ).then((response) => {
                    console.log("response", response.data.data.forecast);
                    // this.weather_list = response.data.data.forecast
                    this.data = response.data.data.forecast
                })

            },
            chart01() {
                console.log(":::", this.$refs.chart01);
                var myChart = echarts.init(this.$refs.chart01);
                var option;
                option = {
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            // Use axis to trigger tooltip
                            type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
                        }
                    },
                    legend: {},
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },
                    xAxis: {
                        type: 'value'
                    },
                    yAxis: {
                        type: 'category',
                        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                    },
                    series: [
                        {
                            name: 'Direct',
                            type: 'bar',
                            stack: 'total',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: [320, 302, 301, 334, 390, 330, 320]
                        },
                        {
                            name: 'Mail Ad',
                            type: 'bar',
                            stack: 'total',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: [120, 132, 101, 134, 90, 230, 210]
                        },
                        {
                            name: 'Affiliate Ad',
                            type: 'bar',
                            stack: 'total',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: [220, 182, 191, 234, 290, 330, 310]
                        },
                        {
                            name: 'Video Ad',
                            type: 'bar',
                            stack: 'total',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: [150, 212, 201, 154, 190, 330, 410]
                        },
                        {
                            name: 'Search Engine',
                            type: 'bar',
                            stack: 'total',
                            label: {
                                show: true
                            },
                            emphasis: {
                                focus: 'series'
                            },
                            data: [820, 832, 901, 934, 1290, 1330, 1320]
                        }
                    ]
                };

                option && myChart.setOption(option);


            },
            chart02() {

                var myChart = echarts.init(this.$refs.chart02);
                var option;
                option = {
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        top: '5%',
                        left: 'center'
                    },
                    series: [
                        {
                            name: 'Access From',
                            type: 'pie',
                            radius: ['40%', '70%'],
                            avoidLabelOverlap: false,
                            itemStyle: {
                                borderRadius: 10,
                                borderColor: '#fff',
                                borderWidth: 2
                            },
                            label: {
                                show: false,
                                position: 'center'
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    fontSize: '40',
                                    fontWeight: 'bold'
                                }
                            },
                            labelLine: {
                                show: false
                            },
                            data: [
                                {value: 1048, name: 'Search Engine'},
                                {value: 735, name: 'Direct'},
                                {value: 580, name: 'Email'},
                                {value: 484, name: 'Union Ads'},
                                {value: 300, name: 'Video Ads'}
                            ]
                        }
                    ]
                };

                option && myChart.setOption(option);


            }
        },


        mounted() {



            this.get_weather();
            this.chart01();
            this.chart02();

        }
    }
</script>

<style scoped>
    .chart {
        height: 500px;
    }
</style>