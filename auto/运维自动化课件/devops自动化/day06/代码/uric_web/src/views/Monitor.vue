<template>
  <div class="schedule">
    <div class="add_app" style="margin-top: 20px">
      <a-button style="margin-bottom: 20px;" @click="showMonitorModal">新增监控主机</a-button>
    </div>

    <a-modal v-model:visible="MonitorModalVisible" title="新增监控主机" @ok="handOk" ok-text="添加" cancel-text="取消">
      <a-form
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="labelCol"
        :wrapper-col="wrapperCol"
      >
        <a-form-item label="主机列表：" prop="hosts">
          <a-select
            mode="multiple"
            v-model:value="form.hosts"
            style="width: 100%"
            placeholder="请选择要监控主机"
          >
            <a-select-option v-for="(host_value,host_index) in host_list" :key="host_index" :value="host_value.id">
             {{host_value.ip_addr}}--{{host_value.name}}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="监控参数：" prop="param">
          <a-select style="width: 120px" v-model:value="form.param" placeholder="请选择要监控的参数类型">
            <a-select-option v-for="(param,key) in monitor_param_choices" :value="param.id" :key="param.id">
              {{param.description}}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item ref="value" label="报警阈值：" prop="value">
          <a-input v-model:value="form.value" style="width: 60px;"/> %
        </a-form-item>
        <a-form-item label="通知类型：" prop="notification_type">
          <a-select style="width: 120px" v-model:value="form.notification_type" placeholder="请选择要监控的参数类型">
            <a-select-option v-for="(notification,index) in notification_type_choices" :value="index" :key="index">
              {{notification[1]}}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item ref="notification_info" label="通知人列表：" prop="notification_info">
          <a-input v-model:value="form.notification_info" />
        </a-form-item>
        <a-form-item ref="times" label="时间间隔：" prop="times">
          <a-input v-model:value="form.times" />
        </a-form-item>
      </a-form>
    </a-modal>

    <div class="release">
      <div class="app_list">
        <a-table :columns="columns" :data-source="MonitorList" row-key="id">
          <template #bodyCell="{ column, text, record }">
            <template v-if="column.dataIndex === 'action'">
              <a @click="showMonitorInfoModal(record)">查看</a>
              <span style="color: lightgray"> | </span>
              <a>删除</a>
            </template>
          </template>
        </a-table>
      </div>
    </div>
    <a-modal v-model:visible="MonitorVisible" :wrap-style="{ overflow: 'hidden' }" width="800px" title="监控窗口" @ok="handleOk">
      <MonitorWindow></MonitorWindow>
    </a-modal>

  </div>
</template>

<script>
import {ref, reactive} from 'vue';
import axios from "axios";
import settings from "@/settings";
import {message} from 'ant-design-vue';
import store from "@/store";
import MonitorWindow from "@/views/MonitorWindow";

export default {
  components: {
    MonitorWindow
  },
  setup() {
    // 表格字段列设置
    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        key: 'id',
        sorter: true,
        width: 100
      },
      {
        title: '监控主机',
        dataIndex: 'host',
        key: 'host',
        sorter: true,
        width: 150
      },
      {
        title: '通知类型',
        dataIndex: 'notification',
        key: 'notification',
        sorter: true,
        width: 150
      },
      {
        title: '监控参数',
        dataIndex: 'param',
        key: 'param',
        sorter: true,
        width: 150
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 300,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]


    // 监控主机列表
    const MonitorList = ref([]);

    const get_tasks_list = ()=>{
      axios.get(`${settings.host}/monitor/host/`,{
        headers:{
          Authorization: "jwt " + store.getters.token
        }
      }).then((res) => {
        let infoList = []
        for (const item of res.data) {
          infoList.push({
            id: item.id,
            notification: item.get_notification_type_display,
            host_id: item.host,
            host: `${item.host_name}[${item.host_ip_addr}:${item.host_port}]`,
            param: item.param_description,
          });
        }
          MonitorList.value = infoList;
      })
    }

    get_tasks_list();

    const labelCol = reactive({span: 4})
    const wrapperCol = reactive({span: 14})
    const other = ref('')
    const monitor_param_choices = ref([])  // 所有监控参数类型数据
    const host_list = ref([]) // 主机列表数据

    const form = reactive({
        hosts: [],
        param: 1,
        value: 0,
        notification_type:0,
        notification_info: '',
        times: 60,
    })

    const rules = reactive({
      task_name: [
        {required: true, message: '请输入任务名称', trigger: 'blur'},
      ],
    })

    // 获取主机列表
    const get_host_list = ()=>{
      axios.get(`${settings.host}/host/`,{
        headers:{
          Authorization: "jwt " + store.getters.token
        }
      }).then((res) => {
          host_list.value = res.data;
      })
    }

    get_host_list();

    // 获取监控参数类型
    const get_monitor_param = ()=>{
      axios.get(`${settings.host}/monitor/param/`,{
        headers:{
          Authorization: "jwt " + store.getters.token
        }
      }).then((res) => {
          monitor_param_choices.value = res.data;
      })
    }
    get_monitor_param()

    // 获取监控参数类型
    const notification_type_choices = ref([])
    const get_notification_type = ()=>{
      axios.get(`${settings.host}/monitor/notif/`,{
        headers:{
          Authorization: "jwt " + store.getters.token
        }
      }).then((res) => {
          notification_type_choices.value = res.data;
      })
    }
    get_notification_type()

    // 是否显示添加监控主机的弹窗
    const MonitorModalVisible = ref(false)
    const showMonitorModal = ()=>{
      MonitorModalVisible.value = true
    }

    // 提交表单
    const handOk = ()=>{
      let hosts = form.hosts
      for (const host of hosts) {
        form['host'] = host
        axios.post(`${settings.host}/monitor/host/`,form, {
          headers:{
            Authorization: "jwt " + store.getters.token
          }
        }).then((res) => {
            message.success("添加监控主机信息成功！")
            MonitorModalVisible.value = false
            MonitorList.value.unshift({
            id: res.data.id,
            notification: res.data.get_notification_type_display,
            host_id: res.data.host,
            host: `${res.data.host_name}[${res.data.host_ip_addr}:${res.data.host_port}]`,
            param: res.data.param_description,
          });
        })
      }
    }

    // 控制是否显示监控窗口
    const MonitorVisible = ref(false)
    const showMonitorInfoModal = (record)=>{
      console.log("显示的监控信息：", record);
      MonitorVisible.value = true;
    }

    return {
      columns,
      labelCol,
      wrapperCol,
      other,
      monitor_param_choices,
      notification_type_choices,
      host_list,
      form,
      rules,
      MonitorList,
      MonitorModalVisible,
      showMonitorModal,
      handOk,
      MonitorVisible,
      showMonitorInfoModal,
    }
  }
}
</script>

<style scoped>

</style>