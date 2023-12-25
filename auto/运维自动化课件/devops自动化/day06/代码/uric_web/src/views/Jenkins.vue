<template>
  <div class="add_app">
    <a-button style="margin: 20px 0;" @click="showAppModal">新建job项目</a-button>
  </div>
  <a-modal v-model:visible="AppModelVisible" title="新建job项目" @ok="handleAddJobOk" ok-text="添加" cancel-text="取消">
    <a-form ref="addJobForm" :model="job_form" :rules="add_job_rules" :label-col="labelCol" :wrapper-col="wrapperCol">
      <a-form-item ref="job_name" label="项目名称" prop="job_name">
        <a-input v-model:value="job_form.job_name"/>
      </a-form-item>
      <a-form-item label="备注信息" prop="description">
        <a-textarea v-model:value="job_form.description"/>
      </a-form-item>
      <a-form-item ref="git" label="Git仓库地址" prop="git">
        <a-input v-model:value="job_form.git"/>
      </a-form-item>
      <a-form-item ref="branch" label="Git分支" prop="branch">
        <a-input v-model:value="job_form.branch"/>
      </a-form-item>
      <a-form-item ref="trigger" label="设置定时构建" prop="trigger">
        <a-input v-model:value="job_form.trigger"/>
      </a-form-item>
      <a-form-item ref="publishers" label="部署环境" prop="publishers">
        <a-select ref="select" v-model:value="job_form.publishers">
          <a-select-option value="u192.168.233.136" key="u192.168.233.136">
            u192.168.233.136
          </a-select-option>
          <a-select-option value="u192.168.233.137" key="u192.168.233.137">
            u192.168.233.137
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="远程主机部署代码的目录" prop="remote_directory">
        <a-input v-model:value="job_form.remote_directory"/>
      </a-form-item>
      <a-form-item label="推送到远程主机的源码文件" prop="source_files">
        <a-input v-model:value="job_form.source_files"/>
      </a-form-item>
      <a-form-item label="构建之前要删除的远程主机目录" prop="remove_prefix">
        <a-input v-model:value="job_form.remove_prefix"/>
      </a-form-item>
      <a-form-item label="构建后执行的Shell命令" prop="command">
        <a-textarea v-model:value="job_form.command"/>
      </a-form-item>
    </a-form>
  </a-modal>

  <div class="release">
    <div class="app_list">
      <a-table :columns="columns" :data-source="jobList" row-key="id">
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'color'">
            <smile-outlined v-if="record.color === 'blue'" style="color: blue; font-size:48px;"/>
            <meh-outlined v-else-if="record.color === 'notbuilt'" style="color: orage; font-size:48px;"/>
            <frown-outlined v-else style="font-size:48px; color: red"/>
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a @click="build_job(record.fullname)">发布</a>
            <span style="color: lightgray"> | </span>
<!--            <a>克隆发布</a>-->
<!--            <span style="color: lightgray"> | </span>-->
            <a>编辑</a>
            <span style="color: lightgray"> | </span>
            <a>删除</a>
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script>
import {ref, reactive, watch} from 'vue';
import axios from "axios";
import settings from "@/settings";
import {message} from 'ant-design-vue';
import store from "@/store";
import {SmileOutlined, MehOutlined, FrownOutlined}  from '@ant-design/icons-vue';
export default {
  components: {
    SmileOutlined,
    MehOutlined,
    FrownOutlined,
  },
  setup() {
    // 搜索栏的表单布局设置
    const formItemLayout = reactive({
      labelCol: {span: 8},
      wrapperCol: {span: 12},
    });

    // 表格字段列设置
    const columns = [
      {
        title: 'job名称',
        dataIndex: 'fullname',
        key: 'fullname',
        sorter: true,
        width: 230
      },
      {
        title: '发布状态',
        dataIndex: 'color',
        key: 'description'
      },
      {
        title: 'job访问地址',
        dataIndex: 'url',
        key: 'url'
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 300,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]

    // 构建项目列表
    const jobList = ref([])

    // 获取构建项目列表
    const get_job_list = ()=>{
      axios.get(`${settings.host}/release/jenkins/`,{
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        jobList.value = response.data;
        console.log(jobList.value)
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }

    get_job_list()

    // 开始构建项目
    const build_job = (job_name)=>{
      axios.put(`${settings.host}/release/jenkins/build/`,{name: job_name},{
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        message.success("构建成功！")
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }

    // 是否显示新建构建项目的弹窗
    const AppModelVisible = ref(false)

    const showAppModal = ()=>{
      AppModelVisible.value = true;
    }

    const labelCol = reactive({
      span: 6
    })

    const wrapperCol = reactive({
      span: 16
    })


    const job_form = reactive({               // 新建发布应用的表单数据
      job_name: "",
      description: "",
      git: "",
      branch: "",
      trigger: "",
      publishers: "",
      remote_directory: "",
      source_files: "",
      remove_prefix: "",
      command: "",
    })

    const add_job_rules = reactive({  // 添加发布应用的表单数据验证规则
        job_name: [
          {required: true, message: '请输入構建項目名称', trigger: 'blur'},
          {min: 1, max: 30, message: '应用名称的长度必须在1~30个字符之间', trigger: 'blur'},
        ],
        git: [
          {required: true, message: '请输入Gitca仓库的地址', trigger: 'blur'},
          {min: 1, max: 150, message: '应用名称的长度必须在1~150个字符之间', trigger: 'blur'},
        ],
    })

    const handleAddJobOk = ()=>{
      // 添加应用的表单提交处理
      axios.post(`${settings.host}/release/jenkins/`,job_form,{
          headers: {
            Authorization: "jwt " + store.getters.token,
          }
        })
        .then((res)=>{
          // JobList.value.push(res.data);
          message.success('新建成功！');
          AppModelVisible.value = false;
        }).catch((error)=>{
          message.error('新建失败！');
        })
    }

    return {
      formItemLayout,
      columns,
      jobList,
      build_job,

      AppModelVisible,
      showAppModal,
      job_form,
      labelCol,
      wrapperCol,
      add_job_rules,
      handleAddJobOk,
    }
  }
}
</script>


<style scoped>
.release_btn span{
  color: #1890ff;
  cursor: pointer;
}
</style>