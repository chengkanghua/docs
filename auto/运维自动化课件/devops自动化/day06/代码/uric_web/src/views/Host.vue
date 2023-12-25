<template>
  <a-row>
    <a-col :span="20">
      <div class="add_host" style="margin: 15px;">
        <a-button @click="showHostModal" type="primary">
          新建
        </a-button>
        <a-button type="primary" @click="showExcelModal" style="margin-left: 20px;">
          批量导入
        </a-button>
        <a-popconfirm
          :title="`确认要删除选中的${hostSelectedRowKeys.length}台主机信息吗？`"
          ok-text="删除"
          cancel-text="取消"
          @confirm="deleteManyHost"
        >
        <a-button type="primary" v-if="hostSelectedRowKeys.length>0" style="margin-left: 20px;">
          批量删除({{hostSelectedRowKeys.length}})
        </a-button>
        </a-popconfirm>
        <a-button type="primary" v-if="hostSelectedRowKeys.length>0" @click="showHostMoveModal" style="margin-left: 20px;">
          移动选中主机({{hostSelectedRowKeys.length}})
        </a-button>
        <a-input v-model:value="search_text" placeholder="请输入要搜索的主机关键信息"  style="float: right; margin-left: 20px; max-width: 240px"/>
      </div>
    </a-col>
  </a-row>

  <a-table :dataSource="hostList.data" :row-selection="rowSelection" row-key="id" :columns="hostFormColumns">
    <template #bodyCell="{ column, text, record }">
       <template v-if="column.dataIndex === 'console'">
        <router-link :to="`/uric/console/${record.id}`">console</router-link>
       </template>

      <template v-if="column.dataIndex === 'action'">
        <a-popconfirm
            v-if="hostList.data.length"
            title="Sure to delete?"
            @confirm="deleteHost(record)"
        >
          <a>Delete</a>
        </a-popconfirm>
        <a style="margin-left: 20px;" @click="showHostUpdateModal(record)">Update</a>
      </template>
    </template>
  </a-table>

  <a-modal v-model:visible="hostFormVisible" title="添加主机" @ok="onHostFormSubmit" @cancel="resetForm()" :width="800">
    <a-form
        ref="formRef"
        name="custom-validation"
        :model="hostForm.form"
        :rules="hostForm.rules"
        v-bind="layout"
        @finish="handleFinish"
        @validate="handleValidate"
        @finishFailed="handleFinishFailed"
    >
      <a-form-item label="主机类别" name="category">
        <a-row>
          <a-col :span="12">
            <a-select
                ref="select"
                v-model:value="hostForm.form.category"
                @change="handleCategorySelectChange"

            >
              <a-select-option :value="category.id" v-for="category in categoryList.data" :key="category.id">
                {{ category.name }}
              </a-select-option>
            </a-select>
          </a-col>

        </a-row>

      </a-form-item>

      <a-form-item label="从属环境" name="environment">
        <a-row>
          <a-col :span="12">
            <a-select
                ref="select"
                v-model:value="hostForm.form.environment"
                @change="handleEnvironmentSelectChange"
            >
              <a-select-option :value="environment.id" v-for="environment in environmentList.data" :key="environment.id">
                {{ environment.name }}
              </a-select-option>
            </a-select>
          </a-col>

        </a-row>

      </a-form-item>

      <a-form-item has-feedback label="主机名称" name="name">
        <a-input v-model:value="hostForm.form.name" type="text" autocomplete="off"/>
      </a-form-item>


      <a-form-item has-feedback label="连接地址" name="username">
        <a-row>
          <a-col :span="8">
            <a-input placeholder="用户名" addon-before="ssh" v-model:value="hostForm.form.username" type="text"
                     autocomplete="off"/>
          </a-col>
          <a-col :span="8">
            <a-input placeholder="ip地址" addon-before="@" v-model:value="hostForm.form.ip_addr" type="text"
                     autocomplete="off"/>
          </a-col>
          <a-col :span="8">
            <a-input placeholder="端口号" addon-before="-p" v-model:value="hostForm.form.port" type="text"
                     autocomplete="off"/>
          </a-col>
        </a-row>
      </a-form-item>

      <a-form-item has-feedback label="连接密码" name="password">
        <a-input v-model:value="hostForm.form.password" type="password" autocomplete="off"/>
      </a-form-item>

      <a-form-item has-feedback label="备注信息" name="description">
        <a-textarea placeholder="请输入主机备注信息" v-model:value="hostForm.form.description" type="text"
                    :auto-size="{ minRows: 3, maxRows: 5 }" autocomplete="off"/>
      </a-form-item>


      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button @click="resetForm">Reset</a-button>
      </a-form-item>
    </a-form>


  </a-modal>
  <a-modal :width="600" title="新建主机类别" :visible="HostCategoryFromVisible" @cancel="hostCategoryFormCancel">
    <template #footer>
      <a-button key="back" @click="hostCategoryFormCancel">取消</a-button>
      <a-button key="submit" type="primary" :loading="loading" @click="onHostCategoryFromSubmit">提交</a-button>
    </template>
    <a-form-model ref="hostCategoryRuleForm" v-model:value="hostCategoryForm.form" :rules="hostCategoryForm.rules"
                  :label-col="hostCategoryForm.labelCol" :wrapper-col="hostCategoryForm.wrapperCol">
      <a-form-model-item ref="name" label="类别名称" name="name">
        <a-row>
          <a-col :span="24">
            <a-input placeholder="请输入主机类别名称" v-model:value="hostCategoryForm.form.name"/>
          </a-col>
        </a-row>
      </a-form-model-item>
    </a-form-model>
  </a-modal>
  <!-- 批量导入主机 -->
  <div>
    <a-modal v-model:visible="excelVisible" title="导入excel批量创建主机" @ok="onExcelSubmit" @cancel="excelFormCancel"
             :width="800">
      <a-alert type="info" message="导入或输入的密码仅作首次验证使用，并不会存储密码。" banner closable/>
      <br/>

      <p>
        <a-form-item has-feedback label="模板下载" help="请下载使用该模板填充数据后导入">
          <a download="主机导入模板.xls">主机导入模板.xls</a>
        </a-form-item>
      </p>
      <p>
        <a-form-item label="默认密码"
                     help="如果Excel中密码为空则使用该密码">
          <a-input v-model:value="default_password" placeholder="请输入默认主机密码" type="password"/>
        </a-form-item>
      </p>
      <a-form-item label="导入数据">
        <div class="clearfix">
          <a-upload
              :file-list="fileList"
              name="file"
              :before-upload="beforeUpload"
          >
            <a-button>
              <upload-outlined></upload-outlined>
              Click to Upload
            </a-button>
          </a-upload>
        </div>
      </a-form-item>
    </a-modal>
    </div>

    <a-modal v-model:visible="hostUpdateFormVisible" title="更新主机" @ok="onHostUpdateFormSubmit" @cancel="resetUpdateForm()" :width="800">
    <a-form
        ref="updateFormRef"
        name="custom-validation"
        :model="hostUpdateForm.form"
        :rules="hostUpdateForm.rules"
        v-bind="layout"
    >
      <a-form-item label="主机类别" name="category">
        <a-row>
          <a-col :span="12">
            <a-select
                ref="select"
                v-model:value="hostUpdateForm.form.category"
                @change="handleCategorySelectChange"
            >
              <a-select-option :value="category.id" v-for="category in categoryList.data" :key="category.id">
                {{ category.name }}
              </a-select-option>
            </a-select>
          </a-col>

        </a-row>
      </a-form-item>
      <a-form-item has-feedback label="主机名称" name="name">
        <a-input v-model:value="hostUpdateForm.form.name" type="text" autocomplete="off"/>
      </a-form-item>
      <a-form-item has-feedback label="连接地址" name="username">
        <a-row>
          <a-col :span="8">
            <a-input placeholder="用户名" addon-before="ssh" v-model:value="hostUpdateForm.form.username" type="text"
                     autocomplete="off"/>
          </a-col>
          <a-col :span="8">
            <a-input placeholder="ip地址" addon-before="@" v-model:value="hostUpdateForm.form.ip_addr" type="text"
                     autocomplete="off"/>
          </a-col>
          <a-col :span="8">
            <a-input placeholder="端口号" addon-before="-p" v-model:value="hostUpdateForm.form.port" type="text"
                     autocomplete="off"/>
          </a-col>
        </a-row>
      </a-form-item>

      <a-form-item has-feedback label="连接密码" name="password">
        <a-input v-model:value="hostUpdateForm.form.password" placeholder="如果更改主机连接地址，必须填写新的连接密码！" type="password" autocomplete="off"/>
      </a-form-item>

      <a-form-item has-feedback label="备注信息" name="description">
        <a-textarea placeholder="请输入主机备注信息" v-model:value="hostUpdateForm.form.description" type="text"
                    :auto-size="{ minRows: 3, maxRows: 5 }" autocomplete="off"/>
      </a-form-item>

      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button @click="resetUpdateForm">Reset</a-button>
      </a-form-item>
    </a-form>
  </a-modal>

  <!-- 批量移动主机 -->
  <a-modal v-model:visible="hostMoveVisible" title="移动主机" @ok="onHostMoveSubmit" @cancel="resetHostMove()" :width="600">
        <a-form-item label="主机类别" name="category">
        <a-row>
          <a-col :span="12">
            <a-select
                ref="select"
                v-model:value="hostMoveForm.category"
                @change="handleCategorySelectChange"
            >
              <a-select-option :value="category.id" v-for="category in categoryList.data" :key="category.id">
                {{ category.name }}
              </a-select-option>
            </a-select>
          </a-col>

        </a-row>
      </a-form-item>
  </a-modal>
</template>

<script>
import {createVNode, ref, reactive, watch} from 'vue';
import axios from "axios";
import settings from "@/settings";
import store from "@/store";
import {Modal, message} from 'ant-design-vue';
import {UploadOutlined, ExclamationCircleOutlined} from '@ant-design/icons-vue';

export default {
  components: {
    UploadOutlined,
  },
  setup() {

    const handleCategorySelectChange = (value) => {
      // 切换主机类别的回调处理
      console.log(value)
    };

    const handleEnvironmentSelectChange = (value)=>{
      // 切换主机所属环境的回调处理
      console.log(value)
    }

    const formRef = ref();
    const HostCategoryFromVisible = ref(false);
    const default_password = ref("");
    const hostList = reactive({  // 主机列表
      data: []
    })
    const categoryList = reactive({  // 主机分类列表
      data: []
    })

    const environmentList = reactive({  // 主机所属环境列表
      data: []
    })

    const hostForm = reactive({
      labelCol: {span: 6},
      wrapperCol: {span: 14},
      other: '',
      form: {
        name: '',
        category: "",
        environment: "", // 新增主机的表单中增加环境id字段
        ip_addr: '',
        username: '',
        port: '',
        description: '',
        password: ''
      },
      rules: {
        name: [
          {required: true, message: '请输入主机名称', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入连接密码', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        category: [
          {required: true, message: '请选择类别', trigger: 'change'}
        ],
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位', trigger: 'blur'}
        ],
        ip_addr: [
          {required: true, message: '请输入连接地址', trigger: 'blur'},
          {max: 30, message: '长度最大15位', trigger: 'blur'}
        ],
        port: [
          {required: true, message: '请输入端口号', trigger: 'blur'},
          {max: 5, message: '长度最大5位', trigger: 'blur'}
        ]
      }
    });

    let validateName = async (_rule, value) => {
      if (value === '') {
        return Promise.reject('请输入类别名称');
      } else {
        return Promise.resolve();
      }
    };

    const hostCategoryForm = reactive({
      labelCol: {span: 6},
      wrapperCol: {span: 14},
      other: '',
      form: {
        name: ''
      },
      rules: {
        name: [{
          required: true,
          message: '请输入类别名称',
          validator: validateName,
          trigger: 'blur'
        },
          {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
        ]
      }
    })

    const layout = {
      labelCol: {
        span: 4,
      },
      wrapperCol: {
        span: 14,
      },
    };

    const hostFormColumns = [
        {
          title: '类别',
          dataIndex: 'category_name',
          key: 'category_name'
        },
        {
          title: '环境',
          dataIndex: 'environment_name',
          key: 'environment_name'
        },
        {
          title: '主机名称',
          dataIndex: 'name',
          key: 'name',
          sorter: true,
          width: 230

        },
        {
          title: '连接地址',
          dataIndex: 'ip_addr',
          key: 'ip_addr',
          ellipsis: true,
          sorter: true,
          width: 150
        },
        {
          title: '端口',
          dataIndex: 'port',
          key: 'port',
          ellipsis: true
        },
        {
          title: 'Console',
          dataIndex: 'console',
          key: 'console',
          ellipsis: true
        },

        {
          title: '操作',
          key: 'action',
          width: 200,
          dataIndex: "action",
          scopedSlots: {customRender: 'action'}
        }
      ]

    const handleFinish = values => {
      console.log(values, hostForm);
    };

    const handleFinishFailed = errors => {
      console.log(errors);
    };

    const resetForm = () => {
      formRef.value.resetFields();
    };

    const handleValidate = (...args) => {
      console.log(args);
    };

    const hostFormVisible = ref(false);
    const excelVisible = ref(false);

    const showHostModal = () => {
      hostFormVisible.value = true;
    };


    const onHostFormSubmit = () => {

      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存

      const formData = new FormData();
      for (let attr in hostForm.form) {
        formData.append(attr, hostForm.form[attr])
      }

      axios.post(`${settings.host}/host/`, formData, {
            headers: {
              Authorization: "jwt " + store.getters.token,
            }
          }
      ).then((response) => {
        console.log("response>>>", response)
        hostList.data.unshift(response.data)

        // 清空
        resetForm()
        hostFormVisible.value = false; // 关闭对话框
        message.success('成功添加主机信息！')

      }).catch((err) => {
        message.error('添加主机失败')
      });
    }

    const deleteHost = record => {
      console.log(record);
      axios.delete(`${settings.host}/host/${record.id}`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        let index = hostList.data.indexOf(record)
        hostList.data.splice(index, 1);

      }).catch(err => {
        message.error('删除主机失败！')
      })


    }

    const showHostCategoryFormModal = () => {
      // 显示添加主机类别的表单窗口
      HostCategoryFromVisible.value = true
    }

    const hostCategoryFormCancel = () => {
      // 添加主机类别的表单取消
      hostCategoryForm.form.name = ""; // 清空表单内容
      HostCategoryFromVisible.value = false // 关闭对话框
    }

    const excelFormCancel = () => {
      excelVisible.value = false
    }

    const onHostCategoryFromSubmit = () => {
      // 添加主机类别的表单提交处理
      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
      axios.post(`${settings.host}/host/category`, hostCategoryForm.form, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        message.success({
          content: "创建主机类别成功!",
          duration: 1,
        }).then(() => {
          console.log("response:::", response)
          categoryList.data.unshift(response.data)
          hostCategoryFormCancel()
        })
      })
    }


    const get_host_list = () => {
      // 获取主机类别列表

      axios.get(`${settings.host}/host`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        hostList.data = response.data
        console.log("hostList.data=", hostList.data)
      }).catch(err => {
        message.error('无法获取主机类别列表信息！')
      })
    }

    const get_category_list = () => {
      // 获取主机类别列表
      axios.get(`${settings.host}/host/category`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        categoryList.data = response.data
      }).catch(err => {
        message.error('无法获取主机类别列表信息！')
      })
    }

    const get_environment_list = () => {
      // 获取主机类别列表
      axios.get(`${settings.host}/conf/env`, {
        headers: {
          Authorization: "jwt " + store.getters.token
        }
      }).then(response => {
        environmentList.data = response.data
      }).catch(err => {
        message.error('无法获取主机所属环境列表信息！')
      })
    }

    // 获取主机列表
    get_host_list()
    get_category_list()
    get_environment_list()

    // 上传excel文件
    const showExcelModal = () => {
      // 显示批量上传主机的窗口
      excelVisible.value = true
    }

    const handleChange = info => {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    };

    const fileList = ref([]);
    const beforeUpload = (file) => {
      // 当用户选择上传文件以后，需要手动把当前文件添加到待上传文件列表this.excel_fileList中
      fileList.value = [...fileList.value, file];
      return false;
    }
    const onExcelSubmit = () => {
      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
      const formData = new FormData();

      console.log("fileList.value:", fileList.value)
      fileList.value.forEach(file => {
        console.log(">>>", file)
        formData.append('host_excel', file);
      });

      axios.post(`${settings.host}/host/excel_host`, formData, {
            headers: {
              Authorization: "jwt " + store.getters.token,
              'Content-Type': 'multipart/form-data', // 上传文件必须设置请求头中的提交内容格式：multipart/form-data
            }
          }
      ).then((response) => {
        console.log("response:::", response)
        console.log("hostList:::", hostList)
        excelFormCancel()// 关闭对话框
        fileList.value = []
        hostList.data.push(...response.data.data)
        message.success('批量创建主机成功!！')

      }).catch((response) => {
        message.error(response.data.message)
      });
    }

    // 更新主机信息
    const hostUpdateForm = reactive({
      labelCol: {span: 6},
      wrapperCol: {span: 14},
      other: '',
      form: {
        id: 0,
        name: '',
        category: "",
        ip_addr: '',
        username: '',
        port: '',
        description: '',
        password: ''
      },
      rules: {
        name: [
          {required: true, message: '请输入主机名称', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入连接密码', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位之间', trigger: 'blur'}
        ],
        category: [
          {required: true, message: '请选择类别', trigger: 'change'}
        ],
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 3, max: 30, message: '长度在3-10位', trigger: 'blur'}
        ],
        ip_addr: [
          {required: true, message: '请输入连接地址', trigger: 'blur'},
          {max: 30, message: '长度最大15位', trigger: 'blur'}
        ],
        port: [
          {required: true, message: '请输入端口号', trigger: 'blur'},
          {max: 5, message: '长度最大5位', trigger: 'blur'}
        ]
      }
    });
    const hostUpdateFormVisible = ref(false);
    const updateFormRef = ref(null);
    const showHostUpdateModal = (record) => {
      hostUpdateForm.form = {...record}
      hostUpdateFormVisible.value = true;
    };
    const onHostUpdateFormSubmit = () => {
      // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
      axios.put(`${settings.host}/host/${hostUpdateForm.form.id}`, hostUpdateForm.form, {
            headers: {
              Authorization: "jwt " + store.getters.token,
            }
          }
      ).then((response) => {
        for(let key in hostList.data){
          if(hostList.data[key].id === hostUpdateForm.form.id){
            hostList.data[key] = {...response.data}
          }
        }
        // 清空
        resetUpdateForm()
        hostUpdateFormVisible.value = false; // 关闭对话框
        message.success('更新主机信息成功！')

      }).catch((err) => {
        message.error('更新主机信息失败！')
      });
    }

    const resetUpdateForm = () => {
      updateFormRef.value.resetFields();
    };

    const hostSelectedRows = ref([]);
    const hostSelectedRowKeys = ref("");
    // 多选操作
    const rowSelection = {
      onChange: (selectedRowKeys, selectedRows) => {
        hostSelectedRowKeys.value = selectedRowKeys
        hostSelectedRows.value = selectedRows
      }
    };

    // 批量删除
    const deleteManyHost = ()=>{
      axios.delete(`${settings.host}/host`, {
          params: {
            id_list: hostSelectedRowKeys.value,
          },
          headers: {
            Authorization: "jwt " + store.getters.token,
          }
        }
      ).then((response) => {
        if(response.data[0]>0){
          [...hostSelectedRowKeys.value].forEach((id, index)=>{
            hostList.data.forEach((host, key)=>{
              if(id === host.id){
                hostList.data.splice(key,1)
              }
            })
          })
        }
        message.success("批量删除主机操作成功！");

      }).catch(error=>{
        console.log("删除失败！");
      })
    }

    // 移动主机
    const hostMoveForm = reactive({
      category: "请选择主机类别",
    })
    const hostMoveVisible = ref(false);
    const showHostMoveModal = () => {
      hostMoveVisible.value = true;
    };
    const onHostMoveSubmit = ()=>{
      console.log(`把id为${hostSelectedRowKeys.value}的主机移动到${hostMoveForm.category}中`);
      axios.patch(`${settings.host}/host/`, {
            id_list: hostSelectedRowKeys.value,
            category: hostMoveForm.category,
          },{
          headers: {
            Authorization: "jwt " + store.getters.token,
          }
        }
      ).then(response=>{
        [...hostSelectedRowKeys.value].forEach((id, index)=>{
          hostList.data.forEach((host, key)=>{
            if(id === host.id){
              [...categoryList.data].filter(category=>{
                if(category.id === hostMoveForm.category){
                  console.log(host);
                  host.category_name=category.name;
                  host.category=category.id;
                }
              })
            }
          })
        })
        hostMoveVisible.value = false;

        hostSelectedRows.value = []
        hostSelectedRowKeys.value = ""
        message.success("移动主机成功！")
      }).catch(error=>{
        message.error("移动主机失败！")
      })
    }
    const resetHostMove = ()=>{
      hostMoveForm.category = "请选择主机类别";
    }

    // 搜索主机功能实现
    const search_text = ref("");
    let timer = ref(null);
    watch(
        search_text,
        ()=>{
          clearTimeout(timer);
          timer = setTimeout(()=>{
            axios.get(`${settings.host}/host/search/`, {
              params: {
                text: search_text.value,
              },
              headers: {
                  Authorization: "jwt " + store.getters.token,
                }
            }).then(response=>{
              hostList.data = response.data;
            })
          }, 600);
        }
    )

    return {
      beforeUpload,
      onExcelSubmit,
      selectHostCategory: ref('yuan'),
      hostForm,
      formRef,
      layout,
      HostCategoryFromVisible,
      handleCategorySelectChange,
      handleFinishFailed,
      handleFinish,
      resetForm,
      handleValidate,
      hostFormVisible,
      excelVisible,
      showHostModal,
      onHostFormSubmit,
      deleteHost,
      showHostCategoryFormModal,
      hostCategoryForm,
      hostCategoryFormCancel,
      excelFormCancel,
      onHostCategoryFromSubmit,
      showExcelModal,
      default_password,
      fileList,
      headers: {
        authorization: 'authorization-text',
      },
      handleChange,
      hostFormColumns,
      hostList,
      categoryList,

      hostUpdateForm,
      hostUpdateFormVisible,
      showHostUpdateModal,
      onHostUpdateFormSubmit,
      updateFormRef,
      resetUpdateForm,

      rowSelection,
      hostSelectedRowKeys,
      deleteManyHost,

      hostMoveVisible,
      showHostMoveModal,
      hostMoveForm,
      onHostMoveSubmit,
      resetHostMove,
      hostSelectedRows,

      search_text,


      environmentList,
      handleEnvironmentSelectChange,
    };
  },
};
</script>