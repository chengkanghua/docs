<template>
  <div class="multi_exec">
    <div>
      <h3>执行主机：</h3>
      <div>
        <a-tag closable @close="close_host(info_index)" v-for="(info,info_index) in show_host_info" :key="info.id">
          {{ `${info.name}(${info.ip_addr}:${info.port})` }}
        </a-tag>
      </div>
    </div>
    <div style="margin-top: 10px;">
      <a-button @click="showModal" icon="plus">从主机列表中选择</a-button>&nbsp;
      <a-button @click="showModal2">从执行模板中选择</a-button>
      <div style="margin: 20px;">
        <a-modal v-model:visible="visible2" title="选择执行模板" @ok="handleOk2" width="960px">
          <div>
            <a-row>
              <a-col :span="10">
                <a-form-item label="模板类别：" :label-col="formItemLayout.labelCol"
                             :wrapper-col="formItemLayout.wrapperCol">
                  <a-select style="width: 160px;" placeholder="请选择" @change="">
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="10">
                <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol"
                             label="模板名称：">
                  <a-input placeholder="请输入"/>
                </a-form-item>
              </a-col>
              <a-col :span="4">
                <a-button type="primary" icon="sync" style="margin-top: 3px;" @click="">刷新</a-button>
              </a-col>
            </a-row>
          </div>
          <div>
            <a-table :columns="tem_columns" :data-source="tem_data" :rowKey="record => record.id"
                     :row-selection="{ radioselectedRow: radioselectedRow, onChange: onSelectChange2,type: 'radio' }">
            </a-table>
          </div>
        </a-modal>
      </div>
      <div>
        <a-modal v-model:visible="MultiExecVisible" title="" @ok="onMultiExecSubmit" @cancel="excelFormCancel"
                 :width="1000">

          <a-row>
            <a-col :span="8">
              <a-form-item label="主机类别：" :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol">
                <a-select style="width: 160px;" placeholder="请选择" v-model="host_form.form.category"
                          @change="has_change_category">
                  <a-select-option :value="value.id" v-for="(value, index) in categorys" :key="value.id">
                    {{ value.name }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="主机别名：">
                <a-input placeholder="请输入"/>
              </a-form-item>
            </a-col>
            <a-col :span="4">
              <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="已选：">
                <span style="margin-left: 8px">
                  <template v-if="hasSelected">
                    {{ `${selectedRowKeys.length}` }}
                  </template>
                </span>
              </a-form-item>
            </a-col>
            <a-col :span="4">
              <a-button type="primary" icon="sync" style="margin-top: 3px;" @click="refresh_data">刷新</a-button>
            </a-col>
          </a-row>
          <div>
            <a-table
                :columns="columns"
                :data-source="data"
                :pagination="false"
                :rowKey="record => record.id"
                :row-selection="{ selectedRowKeys: selectedRowKeys, onChange: onSelectChange }"
            ></a-table>
          </div>

        </a-modal>
      </div>

    </div>

    <v-ace-editor
        v-model:value="content"
        lang="html"
        theme="chrome"
        style="height: 200px"/>
    <div>
      <a-button type="primary" icon="thunderbolt" @click="execute_cmd">开始执行</a-button>
    </div>
    <hr>


  </div>


</template>

<script>

import {VAceEditor} from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/theme-chrome';
import axios from "axios";
import store from "@/store";
import {message} from 'ant-design-vue';

const formItemLayout = {
  labelCol: {span: 8},
  wrapperCol: {span: 14},
};
const columns = [
  {
    // slots: {title: 'customTitle'},
    scopedSlots: {customRender: 'action'},
  }, {
    title: '类别',
    dataIndex: 'category_name',
    key: 'category_name',
  }, {
    title: '主机名称',
    dataIndex: 'name',
    key: 'name',
  }, {
    title: '连接地址',
    dataIndex: 'ip_addr',
    key: 'ip_addr',
    width: 200,
  }, {
    title: '端口',
    dataIndex: 'port',
    key: 'port',
  }, {
    title: '备注信息',
    dataIndex: 'description',
    key: 'description',
  },
];

const tem_columns = [
  {
    title: '模板名称',
    dataIndex: 'name',
    key: 'name',

  },
  {
    title: '模板类型',
    dataIndex: 'category_name',
    key: 'category_name',

  },
  {
    title: '模板内容',
    dataIndex: 'cmd',
    key: 'cmd',
    width: 200,
  },
  {
    title: '描述信息',
    dataIndex: 'description',
    key: 'description',

  },
];


export default {
  name: "MultiExec",
  data() {
    return {

      formItemLayout,        // 弹窗的首行表单配置信息
      columns,               // 弹窗的表格的每一列数据的配置信息
      show_host_info: [],    // 显示选中的所有主机内容
      MultiExecVisible: false,        // 是否显示主机列表的弹窗
      host_form: {
        form: {
          category: undefined,// 当前选择的主机分类ID
        }
      },
      data: [],              // 当前显示表格中的主机列表数据
      categorys: [],         // 主机分类列表
      selectedRowKeys: [],   // 已经勾选的主机ID列表
      selected_host_ids: [], // 选中的主机id列表
      visible2: false,
      template_form: {
        form: {
          category: undefined,
        }
      },
      tem_categorys: [],    // 指令模板分类列表
      tem_data: [],         // 指令模板列表
      radioselectedRow: [], //
      content: "",
      tem_columns,
    }
  }
  ,
// 计算属性
  computed: {
    hasSelected() {
      return this.selectedRowKeys.length > 0;
    }
    ,
  }
  ,
  created() {
    this.get_host_category_list()
    this.get_host_list()
    this.get_templates_category_list()
    this.get_templates_list()
  }
  ,
  methods: {
    showModal() {
      this.MultiExecVisible = true;
    }
    ,
    // 选中主机时触发的，selectedRowKeys被选中的主机id列表
    onSelectChange(selectedRowKeys) {
      this.selectedRowKeys = selectedRowKeys;
    }
    ,
    onMultiExecSubmit() {
      this.data.forEach((v, k) => {
        if (this.selectedRowKeys.includes(v.id)) { // 判断某元素是否在数组中用includes比较合适，不能用in
          this.show_host_info.push({
            id: v.id,
            name: v.name,
            ip_addr: v.ip_addr,
            port: v.port,
          })
          this.selected_host_ids.push(v.id);
        }
      })
      // 关闭弹窗
      this.MultiExecVisible = false;
    }
    ,
    get_host_category_list() {
      // 获取主机类别
      // let token = sessionStorage.token || localStorage.token;
      axios.get(`${this.$settings.host}/host/category`, {
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      }).then((response) => {
        this.categorys = response.data;
      })
    }
    ,
    get_host_list(category = null) {
      // 获取主机列表
      let params = {}
      if (category !== null) {
        params.category = category
      }
      // let token = sessionStorage.token || localStorage.token;
      axios.get(`${this.$settings.host}/host/`, {
        params: params,
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      }).then((response) => {
        this.data = response.data;
      })
    }
    ,
    has_change_category(category) {
      // 切换主机分类时，重新获取主机列表
      this.get_host_list(category)
    }
    ,
    refresh_data() {
      // 刷新数据
      this.host_form.form.category = undefined
      this.get_host_list();
    }
    ,
    close_host(info_index) {
      // 移除已经勾选的主机信息
      this.show_host_info.splice(info_index, 1);
      let ids_list = this.selected_host_ids.splice(info_index, 1);
      let id_index = this.selectedRowKeys.indexOf(ids_list[0]);
      this.selectedRowKeys.splice(id_index, 1);
    }
    ,
    execute_cmd() {
      // let token = sessionStorage.token || localStorage.token;
      axios.post(`${this.$settings.host}/mtask/cmd_exec`, {
        host_ids: this.selected_host_ids,
        cmd: this.content,
      }, {
        headers: {
          Authorization: "jwt " + store.getters.token,
        }
      }).then((res) => {
        console.log(res);
        message.success('批量任务执行成功！')

      }).catch((err) => {
        message.error('批量任务执行失败！')
      })
    },


    showModal2() {
      this.visible2 = true;
    },
    handleOk2(e) {
      let tid = this.radioselectedRow[0]; //选中的模板id值
      // 通过模板id值，找到该模板记录中的cmd值，并赋值给content属性
      this.tem_data.forEach((v, k) => {
        if (v.id === tid) {
          this.content = v.cmd;
        }
      })
      this.visible2 = false;
    },
    onSelectChange2(radioselectedRow) {
      // [6, 7, 8, 9]
      console.log('>>>>> ', radioselectedRow);
      this.radioselectedRow = radioselectedRow;
    },
    handleSelectChange2(value) {
      // 切换模板分类
      this.get_templates_list(value)
    },
    refresh_data2() {
      this.get_templates_list();
    },
    get_templates_list(category = null) {
      let params = {}
      if (category !== null) {
        params.category = category
      }
      axios.get(`${this.$settings.host}/mtask/templates`, {
        params: params,
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        this.tem_data = response.data;
      })
    },
    get_templates_category_list() {
      axios.get(`${this.$settings.host}/mtask/templates/categorys`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      })
          .then(response => {
            this.tem_categorys = response.data;
          })
    },
  }
  ,
  components: {
    VAceEditor,
  }
  ,
}
</script>

<style>

</style>