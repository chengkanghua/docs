<template>
  <div class="chart" ref="echartDiv" style="width: 800px; height: 350px;"></div>
</template>

<script>
import {ref, reactive, onMounted} from 'vue';
import * as echarts from 'echarts';

export default {
  name: "MonitorWindow",
  setup(){
    const echartDiv = ref()
    const host_monitor_data = ref([])
    const get_data = ()=>{
      host_monitor_data.value = [
          {name: "2022-11-11 11:01:00", "value": ["2022-11-11 11:01:00", 10]},
          {name: "2022-11-11 11:01:30", "value": ["2022-11-11 11:01:30", 20]},
          {name: "2022-11-11 11:02:00", "value": ["2022-11-11 11:02:00", 30]},
          {name: "2022-11-11 11:02:30", "value": ["2022-11-11 11:02:30", 40]},
          {name: "2022-11-11 11:03:00", "value": ["2022-11-11 11:03:00", 50]},
          {name: "2022-11-11 11:03:30", "value": ["2022-11-11 11:03:30", 30]},
      ]
    }

    get_data();

    const showEchart = ()=>{
      let myChart = echarts.init(echartDiv.value);
      let option = {
        title: {
          text: '监控显示器'
        },
        tooltip: {
          trigger: 'axis',
          formatter(params) {
            params = params[0];
            let date = new Date(params.name);
            return (
              date.getDate() +
              '/' +
              (date.getMonth() + 1) +
              '/' +
              date.getFullYear() +
              ' ' +
              date.getHours() +
              ':' +
              date.getMinutes() +
              ':' +
              date.getSeconds() +
              '  ' +
              params.value[1]
            );
          },
          axisPointer: {
            animation: false
          }
        },
        xAxis: {
          type: 'time',
          splitLine: {
            show: false
          }
        },
        yAxis: {
          type: 'value',
          boundaryGap: [0, '100%'],
          splitLine: {
            show: false
          }
        },
        series: [
          {
            name: 'Fake Data',
            type: 'line',
            showSymbol: false,
            data: host_monitor_data.value
          }
        ]
      };
      option && myChart.setOption(option);
    }

    onMounted(()=>{
      showEchart()
    })

    return {
      echartDiv,
    }
  }
}
</script>

<style scoped>

</style>