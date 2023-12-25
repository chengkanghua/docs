<template>
  <a-row>
    <a-col :span="20">
      <div class="add_host" style="margin: 15px;">
        <a-button @click="showProjectModal" type="primary">
          新建
        </a-button>
      </div>
    </a-col>
  </a-row>
  <div class="release">
    <div class="app_list">
      <a-table :columns="columns" :data-source="gitList" row-key="id">
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'name'">
            <LockOutlined v-if="record.visibility==='private'"></LockOutlined>
            <TeamOutlined v-if="record.visibility==='internal'"></TeamOutlined>
            <GlobalOutlined v-if="record.visibility==='public'"></GlobalOutlined>
             {{record.name}}
          </template>
          <template v-if="column.dataIndex === 'owner'">
            <a :href="record.web_url">{{record.owner?.name}}</a>
          </template>
          <template v-if="column.dataIndex === 'web_url'">
            <a :href="record.web_url">{{record.web_url}}</a>
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a @click="showBranchModal(record)">分支管理</a>
            <span style="color: lightgray"> | </span>
            <a @click="showCommitModal(record)">历史版本</a>
            <span style="color: lightgray"> | </span>
            <a>编辑</a>
            <span style="color: lightgray"> | </span>
            <a>删除</a>
          </template>
        </template>
      </a-table>
    </div>
  </div>
  <!-- 分支管理 -->
  <a-modal v-model:visible="branchVisible" width="1000px" title="分支管理">
    <a-table :columns="branchColumns" :data-source="branchList" row-key="id">
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'web_url'">
            <a :href="record.web_url">{{record.web_url}}</a>
          </template>
          <template v-if="column.dataIndex === 'commit'">
            <span :title="record.commit.id">{{record.commit.short_id}}</span>
            <span style="color: lightgray"> | </span>
            <span>{{record.commit.committer_name}}</span>
            <span style="color: lightgray"> | </span>
            <span>{{record.commit.message}}</span>
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a>编辑</a>
            <span style="color: lightgray"> | </span>
            <a>删除</a>
          </template>
        </template>
      </a-table>
  </a-modal>
  <!-- commit历史版本管理 -->
  <a-modal v-model:visible="commitVisible" width="1000px" title="历史版本管理">
    <a-table :columns="commitColumns" :data-source="commitList" row-key="id">
        <template #bodyCell="{ column, text, record }">
          <template v-if="column.dataIndex === 'short_id'">
            <a-tooltip placement="top">
            <template #title>
              <span>{{record.id}}</span>
            </template>
            <span>{{record.short_id}}</span>
            </a-tooltip>
          </template>
          <template v-if="column.dataIndex === 'web_url'">
            <a :href="record.web_url">{{record.web_url}}</a>
          </template>
          <template v-if="column.dataIndex === 'action'">
            <a>编辑</a>
            <span style="color: lightgray"> | </span>
            <a>删除</a>
          </template>
        </template>
      </a-table>
  </a-modal>
  <!-- 添加项目 -->
  <a-modal v-model:visible="projectModelVisible" title="新建仓库" @ok="handleadProjectOk" ok-text="添加" cancel-text="取消">
    <a-form ref="addProjectRuleForm" :model="project_form" :rules="add_project_rules" :label-col="labelCol" :wrapper-col="wrapperCol">
      <a-form-item ref="name" label="仓库名称" prop="name">
        <a-input v-model:value="project_form.name"/>
      </a-form-item>
      <a-form-item ref="path" label="仓库路径" prop="path">
        <a-input v-model:value="project_form.path"/>
      </a-form-item>
      <a-form-item label="仓库描述" prop="description">
        <a-textarea v-model:value="project_form.description"/>
      </a-form-item>
      <a-form-item ref="default_branch" label="默认分支" prop="default_branch">
        <a-select ref="select" v-model:value="project_form.default_branch">
          <a-select-option value="main" key="main">
            main
          </a-select-option>
          <a-select-option value="master" key="master">
            master
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item ref="visibility" label="可见度" prop="visibility">
        <a-select ref="select" v-model:value="project_form.visibility">
          <a-select-option :value="key" v-for="(visibility,key) in visibility_list" :key="key">
            {{ visibility }}
          </a-select-option>
        </a-select>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script>
import {ref, reactive, watch} from 'vue';
import axios from "axios";
import settings from "@/settings";
import {message} from 'ant-design-vue';
import store from "@/store";
import {GlobalOutlined, LockOutlined, TeamOutlined} from '@ant-design/icons-vue';

export default {
  name: "Git",
  components:{
    GlobalOutlined,
    LockOutlined,
    TeamOutlined,
  },
  setup(){
    // git项目的表格字段列设置
    const columns = [
      {
        title: 'ID',
        dataIndex: 'id',
        key: 'id',
        sorter: true,
        width: 100
      },
      {
        title: '项目名称',
        dataIndex: 'name',
        key: 'name',
        sorter: true,
        width: 200
      },
      {
        title: '项目地址',
        dataIndex: 'web_url',
        key: 'web_url'
      },
      {
        title: '项目所有者',
        dataIndex: 'owner',
        key: 'owner',
        sorter: true,
        width: 150
      },
      {
        title: '描述信息',
        dataIndex: 'description',
        key: 'description'
      },
      {
        title: 'forks',
        dataIndex: 'forks_count',
        key: 'forks_count'
      },
      {
        title: 'star',
        dataIndex: 'star_count',
        key: 'star_count'
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 400,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]

    // git仓库列表
    const gitList = ref([])

    // 获取git仓库列表
    const get_git_list = (searchForm)=>{
      axios.get(`${settings.host}/release/gitlab/`,{
        params: searchForm,
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        gitList.value = response.data;
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }

    get_git_list()


    // 分支管理
    const branchColumns = [
      {
        title: '分支名称',
        dataIndex: 'name',
        key: 'name',
        sorter: true,
        width: 150
      },
      {
        title: '最新Commit版本',
        dataIndex: 'commit',
        key: 'commit'
      },
      {
        title: '分支地址',
        dataIndex: 'web_url',
        key: 'web_url'
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 200,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]

    // 分支列表
    const branchList = ref([])
    // 获取指定git仓库的分支列表
    const get_branch_list = ()=>{
      axios.get(`${settings.host}/release/gitlab/${current_project_id.value}/branchs/`,{
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        branchList.value = response.data;
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }

    const current_project_id = ref("")
    const branchVisible = ref(false)
    const showBranchModal = (record)=>{
      current_project_id.value = record.id
      get_branch_list()
      branchVisible.value = true
    }


    // 历史版本管理
    const commitVisible = ref(false)
    const showCommitModal = (record)=>{
      current_project_id.value = record.id
      get_commit_list()
      commitVisible.value = true;
    }
    const commitColumns = [
      {
        title: '版本ID',
        dataIndex: 'short_id',
        key: 'short_id',
        sorter: true,
        width: 150
      },
      {
        title: '版本描述',
        dataIndex: 'message',
        key: 'message'
      },
      {
        title: '提交者',
        dataIndex: 'committer_name',
        key: 'committer_name'
      },
      {
        title: '操作',
        dataIndex: 'action',
        width: 200,
        key: 'action', scopedSlots: {customRender: 'action'}
      },
    ]

    // 历史版本
    const commitList = ref([])
    const get_commit_list = ()=>{
      // 获取指定仓库的历史版本
      axios.get(`${settings.host}/release/gitlab/${current_project_id.value}/commits/`,{
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      })
      .then(response=>{
        commitList.value = response.data;
      }).catch((error)=>{
        message.error(error.response.data)
      })
    }


    // 添加git项目/仓库
    const projectModelVisible = ref(false)
    const showProjectModal = ()=>{
      projectModelVisible.value = true
    }

    // 新建仓库的表单内容
    const project_form = reactive({
      name:"",
      path:"",
      description:"",
      default_branch:"master",
      visibility:"private",
    })

    const visibility_list = reactive({
        "private": "私有仓库",
        "internal": "内部仓库",
        "public": "公开仓库"
    })

    const labelCol = reactive({span: 6})
    const wrapperCol = reactive({span: 14})

    const add_project_rules = reactive({  // 添加发布应用的表单数据验证规则
        name: [
          {required: true, message: '请输入仓库名称', trigger: 'blur'},
          {min: 1, max: 30, message: '仓库名称的长度必须在1~30个字符之间', trigger: 'blur'},
        ],
        path: [
          {required: true, message: '请输入仓库路径', trigger: 'blur'},
          {min: 1, max: 50, message: '仓库路径的长度必须在1~50个字符之间', trigger: 'blur'},
        ]
    })


    const handleadProjectOk = ()=>{
      // 添加应用的表单提交处理
      axios.post(`${settings.host}/release/gitlab/`, project_form,{
          headers: {
            Authorization: "jwt " + store.getters.token,
          }
        })
        .then((res)=>{
          gitList.value.push(res.data);
          message.success('添加成功！');
          projectModelVisible.value = false;
        }).catch((error)=>{
          message.error('添加失败！');
        })
    }


    return {
      columns,
      gitList,

      branchList,
      branchVisible,
      showBranchModal,
      branchColumns,

      commitVisible,
      commitColumns,
      showCommitModal,
      commitList,

      projectModelVisible,
      showProjectModal,
      project_form,
      visibility_list,
      labelCol,
      wrapperCol,
      add_project_rules,
      handleadProjectOk,
    }
  }
}
</script>

<style scoped>

</style>