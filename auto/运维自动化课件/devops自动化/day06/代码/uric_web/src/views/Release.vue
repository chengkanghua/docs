<template>
  <div class="search" style="margin-top: 15px;">
    <a-row>
      <a-col :span="6">
        <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="应用名称：">
          <a-input v-model:value="searchForm.app_name" placeholder="请输入"/>
        </a-form-item>
      </a-col>
      <a-col :span="6">
        <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="标记符：">
          <a-input v-model:value="searchForm.tag" placeholder="请输入"/>
        </a-form-item>
      </a-col>
      <a-col :span="6">
        <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="描述信息：">
          <a-input v-model:value="searchForm.description" placeholder="请输入"/>
        </a-form-item>
      </a-col>
      <a-col :span="6">
        <router-link to="/release">
          <a-button type="primary" style="margin-top: 3px;">刷新</a-button>
        </router-link>
      </a-col>
    </a-row>
  </div>

  <div class="add_app">
    <a-button style="margin-bottom: 20px;" @click="showAppModal">新建应用</a-button>
  </div>
  <a-modal v-model:visible="AppModelVisible" title="新建应用" @ok="handleaddappOk" ok-text="添加" cancel-text="取消">
    <a-form ref="addappruleForm" :model="app_form" :rules="add_app_rules" :label-col="labelCol" :wrapper-col="wrapperCol">
      <a-form-item ref="app_name" label="应用名称" prop="app_name">
        <a-input v-model:value="app_form.app_name"/>
      </a-form-item>
      <a-form-item ref="tag" label="唯一标识符" prop="tag"><a-input v-model:value="app_form.tag"/>
      </a-form-item>
      <a-form-item label="备注信息" prop="app_desc">
        <a-textarea v-model:value="app_form.app_desc"/>
      </a-form-item>
    </a-form>
  </a-modal>

  <div class="release">
    <div class="app_list">
      <a-table :columns="columns" :data-source="releaseAppList" row-key="id">
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'action'">
            <a>新建发布</a>
            <span style="color: lightgray"> | </span>
            <a>克隆发布</a>
            <span style="color: lightgray"> | </span>
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

export default {
  setup() {
    // 搜索栏的表单布局设置
    const formItemLayout = reactive({
      labelCol: {span: 8},
      wrapperCol: {span: 12},
    });

    // 表格字段列设置
    const columns = [
      {
        title: '应用名称',
        dataIndex: 'name',
        key: 'name',
        sorter: true,
        width: 230
      },
      {
        title: '标识符',
        dataIndex: 'tag',
        key: 'tag',
        sorter: true,
        width: 150
      },
      {
        title: '描述信息',
        dataIndex: 'description',
        key: 'description'
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 300,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]

    // 发布应用列表
    const releaseAppList = ref([])

    // 获取发布应用列表
    const get_release_app_list = (searchForm)=>{
      axios.get(`${settings.host}/release/app/`,{
        params: searchForm,
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        releaseAppList.value = response.data;
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }

    get_release_app_list()

    // 是否显示新建发布应用的弹窗
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


    const app_form = reactive({               // 新建发布应用的表单数据
        app_name: '',
        tag: '',
        app_desc: '',
    })

    const add_app_rules = reactive({  // 添加发布应用的表单数据验证规则
        app_name: [
          {required: true, message: '请输入应用名称', trigger: 'blur'},
          {min: 1, max: 30, message: '应用名称的长度必须在1~30个字符之间', trigger: 'blur'},
        ],
        tag: [
          {required: true, message: '请输入应用唯一标识符', trigger: 'blur'},
          {min: 1, max: 50, message: '应用名称的长度必须在1~50个字符之间', trigger: 'blur'},
        ],
    })

    const handleaddappOk = ()=>{
      // 添加应用的表单提交处理
      let data = {
        name: app_form.app_name,
        tag: app_form.tag,
        description: app_form.app_desc,
      }
      axios.post(`${settings.host}/release/app/`,data,{
          headers: {
            Authorization: "jwt " + store.getters.token,
          }
        })
        .then((res)=>{
          releaseAppList.value.push(res.data);
          message.success('添加成功！');
          AppModelVisible.value = false;
        }).catch((error)=>{
          message.error('添加失败！');
        })
    }

    // 应用搜索
    const searchForm = reactive({
      app_name: "",
      description: "",
      tag: "",
    })

    // 监听搜索框的输入内容
    watch(
        searchForm,
        ()=>{
          get_release_app_list(searchForm)
        }
    )

    return {
      formItemLayout,

      columns,
      releaseAppList,

      AppModelVisible,
      showAppModal,
      app_form,
      labelCol,
      wrapperCol,
      add_app_rules,
      handleaddappOk,
      searchForm,
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