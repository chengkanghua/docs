<template>
    <div class="host">
        <a-card size="small" :bordered="false">
            <a-row>

                <a-col :span="6">
                    <div class="add_host" style="margin-bottom: 15px;">

                        <a-button type="primary" @click="showHostFormModal">
                            新建
                        </a-button>
                        <a-button type="primary" icon="import" style="margin-left: 20px;">
                            批量导入
                        </a-button>
                    </div>
                </a-col>

                <a-col :span="6">
                    <a-form-item label="主机类别：" :label-col="HostFilterFormItemLayout.labelCol"
                                 :wrapper-col="HostFilterFormItemLayout.wrapperCol">
                        <a-select style="width: 100%;" @change="handleCategorySelectChange"
                                  v-model="hostForm.form.host_category_id">
                            <a-select-option :value="category.id" v-for="category in category_list" :key="category.id">
                                {{ category.name }}
                            </a-select-option>
                        </a-select>
                    </a-form-item>
                </a-col>
            </a-row>


            <a-modal
                    :width="800"
                    title="新建主机"
                    :visible="HostFromVisible"
                    @cancel="hostFormCancel"
            >
                <template slot="footer">
                    <a-button key="back" @click="hostFormCancel">取消</a-button>
                    <a-button key="submit" type="primary" :loading="HostFormLoading" @click="onHostFromSubmit">提交
                    </a-button>
                </template>
                <a-form-model ref="hostRuleForm" :model="hostForm.form" :rules="hostForm.rules"
                              :label-col="hostForm.labelCol"
                              :wrapper-col="hostForm.wrapperCol">

                    <a-form-model-item label="主机类别" prop="zone">
                        <a-row>
                            <a-col :span="12">
                                <a-select v-model="hostForm.form.host_category_id" placeholder="请选择主机类别/区域/分组">
                                    <a-select-option :value="category.id" v-for="category in category_list"
                                                     :key="category.id">
                                        {{ category.name }}
                                    </a-select-option>
                                </a-select>
                            </a-col>
                            <a-col :span="6" :offset="2">
                                <a-button @click.stop.prevent="showHostCategoryFormModal"><span>添加类别</span></a-button>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item ref="name" label="主机名称" prop="name">
                        <a-row>
                            <a-col :span="24">
                                <a-input placeholder="请输入主机名称" v-model="hostForm.form.name"/>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item ref="ip_addr" label="连接地址" prop="ip_addr">
                        <a-row>
                            <a-col :span="8">
                                <a-input placeholder="用户名" addon-before="ssh" v-model="hostForm.form.username"/>
                            </a-col>
                            <a-col :span="8">
                                <a-input placeholder="ip地址" addon-before="@" v-model="hostForm.form.ip_addr"/>
                            </a-col>
                            <a-col :span="8">
                                <a-input placeholder="端口号" addon-before="-p" v-model="hostForm.form.port"/>
                            </a-col>
                        </a-row>
                    </a-form-model-item>

                    <a-form-model-item ref="password" label="连接密码" prop="password">
                        <a-row>
                            <a-col :span="24">
                                <a-input placeholder="请输入连接密码" v-model="hostForm.form.password" type="password"/>
                            </a-col>
                        </a-row>
                    </a-form-model-item>

                    <a-form-model-item extra="默认使用全局密钥，如果上传了独立密钥则优先使用该密钥。" ref="name" label="独立秘钥" prop="pkey">
                        <a-row>
                            <a-col :span="24">
                                <a-upload name="file" :multiple="true" action="上传文件的地址" :headers="upload_pkey_headers"
                                          @change="handleFileChange">
                                    <a-button>
                                        <a-icon type="upload"/>
                                        点击上传
                                    </a-button>
                                </a-upload>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item ref="remark" label="备注信息" prop="remark">
                        <a-row>
                            <a-col :span="24">
                                <a-textarea v-model="hostForm.form.remark" placeholder="请输入主机备注信息"
                                            :auto-size="{ minRows: 3, maxRows: 5 }"/>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                    <a-form-model-item>
                        <a-row>
                            <a-col :span="24" :offset="10">
                                <span><a-icon type="warning" style="color:yellow;"/>首次验证时需要输入登录用户名对应的密码，但不会存储该密码。</span>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                </a-form-model>
            </a-modal>
            <a-modal
                    :width="600"
                    title="新建主机类别"
                    :visible="HostCategoryFromVisible"
                    @cancel="hostCategoryFormCancel"
            >
                <template slot="footer">
                    <a-button key="back" @click="hostCategoryFormCancel">取消</a-button>
                    <a-button key="submit" type="primary" :loading="HostCategoryFormLoading"
                              @click="onHostCategoryFromSubmit">
                        提交
                    </a-button>
                </template>
                <a-form-model ref="hostCategoryRuleForm" :model="hostCategoryForm.form" :rules="hostCategoryForm.rules"
                              :label-col="hostCategoryForm.labelCol" :wrapper-col="hostCategoryForm.wrapperCol">
                    <a-form-model-item ref="name" label="类别名称" prop="name">
                        <a-row>
                            <a-col :span="24">
                                <a-input placeholder="请输入主机类别名称" v-model="hostCategoryForm.form.name"/>
                            </a-col>
                        </a-row>
                    </a-form-model-item>
                </a-form-model>
            </a-modal>
            <a-table :columns="hostFormColumns" :data-source="data" rowKey="id">
                <a slot="name" slot-scope="text">{{ text }}</a>
                <template v-slot:action>
                    <a href="javascript:;">编辑</a> |
                    <a href="javascript:;">删除</a> |
                    <a href="javascript:;">Console</a>
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script>
    // 过滤主机信息的表单布局
    const HostFilterFormItemLayout = {
        labelCol: {span: 6},
        wrapperCol: {span: 12}
    }

    // 添加主机表单的字段信息
    const hostFormColumns = [
        {
            title: '类别',
            dataIndex: 'category_name',
            key: 'category_name'
        },
        {
            title: '主机名称',
            dataIndex: 'name',
            key: 'name',
            sorter: true

        },
        {
            title: '连接地址',
            dataIndex: 'ip_addr',
            key: 'ip_addr',
            ellipsis: true,
            sorter: true,
            width: 200
        },
        {
            title: '端口',
            dataIndex: 'port',
            key: 'port',
            ellipsis: true
        },
        {
            title: '备注信息',
            dataIndex: 'remark',
            key: 'remark',
            ellipsis: true
        },

        {
            title: '操作',
            key: 'action',
            width: 200,
            scopedSlots: {customRender: 'action'}
        }
    ]

    export default {
        name: 'Host',
        data() {
            return {
                // 添加主机表单
                HostFormLoading: false, // 是否显示确认按钮的加载状态效果
                HostFilterFormItemLayout, // 添加主机的表单的表单布局: hostFormItemLayout,
                HostFromVisible: false, // 是否显示添加主机的弹窗
                checkIpAddr: false, // 是否验证信息
                // 添加主机类别
                HostCategoryFromVisible: false, // 是否显示添加主机类别的弹窗
                HostCategoryFormLoading: false, // 是否显示确认按钮的加载状态效果
                category_list: [ // 主机类别
                    {'id': 1, 'name': '数据库服务'},
                    {'id': 2, 'name': '缓存服务'},
                    {'id': 3, 'name': 'web服务'},
                    {'id': 4, 'name': '静态文件存储服务'}
                ],
                data: [
                    {
                        'id': 1,
                        'category_name': '数据库服务器',
                        'name': 'izbp13e05jqwodd605vm3gz',
                        'ip_addr': '47.58.131.12',
                        'port': 22,
                        'remark': ''
                    },
                    {
                        'id': 2,
                        'category_name': '数据库服务器',
                        'name': 'iZbp1a3jw4l12ho53ivhkkZ',
                        'ip_addr': '12.18.125.22',
                        'port': 22,
                        'remark': ''
                    },
                    {
                        'id': 3,
                        'category_name': '缓存服务器',
                        'name': 'iZbp1b1xqfqw257gs563k2iZ',
                        'ip_addr': '12.19.135.130',
                        'port': 22,
                        'remark': ''
                    },
                    {
                        'id': 4,
                        'category_name': '缓存服务器',
                        'name': 'iZbp1b1jw4l01ho53muhkkZ',
                        'ip_addr': '47.98.101.89',
                        'port': 22,
                        'remark': ''
                    }
                ],
                hostFormColumns: hostFormColumns, // 主机信息列表的表格表头信息
                // 上传文件的配置参数
                upload_pkey_headers: {
                    authorization: 'authorization-text'
                },
                // 添加主机需要的数据属性
                hostForm: {
                    labelCol: {span: 6},
                    wrapperCol: {span: 14},
                    other: '',
                    form: {
                        name: '',
                        host_category_id: '',
                        ip_addr: '',
                        username: '',
                        port: '',
                        remark: '',
                        password: ''
                    },
                    rules: {
                        name: [
                            {required: true, message: '请输入主机名称', trigger: 'blur'},
                            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
                        ],
                        password: [
                            {required: true, message: '请输入连接密码', trigger: 'blur'},
                            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
                        ],
                        host_category_id: [
                            {required: true, message: '请选择类别', trigger: 'change'}
                        ],
                        username: [
                            {required: true, message: '请输入用户名', trigger: 'blur'},
                            {min: 3, max: 10, message: '长度在3-10位', trigger: 'blur'}
                        ],
                        ip_addr: [
                            {required: true, message: '请输入连接地址', trigger: 'blur'},
                            {max: 15, message: '长度最大15位', trigger: 'blur'}
                        ],
                        port: [
                            {required: true, message: '请输入端口号', trigger: 'blur'},
                            {max: 5, message: '长度最大5位', trigger: 'blur'}
                        ]
                    }
                },
                // 添加主机类别需要的数据属性
                hostCategoryForm: {
                    labelCol: {span: 6},
                    wrapperCol: {span: 14},
                    other: '',
                    form: {
                        name: ''
                    },
                    rules: {
                        name: [
                            {required: true, message: '请输入类别名称', trigger: 'blur'},
                            {min: 3, max: 10, message: '长度在3-10位之间', trigger: 'blur'}
                        ]
                    }
                }
            }
        },
        methods: {
            handleCategorySelectChange(value) {
                // 切换主机类别的回调处理
                console.log(value)
            },
            showHostFormModal() {
                // 显示添加主机的表单窗口
                this.HostFromVisible = true
            },
            showHostCategoryFormModal() {
                // 显示添加主机类别的表单窗口
                this.HostCategoryFromVisible = true
            },
            hostFormCancel(e) {

                // 添加主机的表单取消
                // this.resetHostForm() // 清空表单内容
                this.resetHostForm()
                this.HostFromVisible = false // 关闭对话框
            },
            hostCategoryFormCancel() {
                // 添加主机类别的表单取消
                this.resetHostCategoryForm() // 清空表单内容
                this.HostCategoryFromVisible = false // 关闭对话框
            },
            onHostFromSubmit() {
                // 添加主机的表单提交处理
                this.$refs.hostRuleForm.validate(valid => {
                    // 验证
                    if (valid) {
                        // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
                        // this.$axios.post(`${this.$settings.host}/host/`)
                        // 发送验证请求

                    } else {
                        // 验证失败！
                        return false
                    }
                })
            },
            onHostCategoryFromSubmit() {
                // 添加主机类别的表单提交处理
                this.$refs.hostCategoryRuleForm.validate(valid => {
                    // 验证
                    if (valid) {
                        // 将数据提交到后台进行保存，但是先进行连接校验，验证没有问题，再保存
                        // this.$axios.post(`${this.$settings.host}/host_category/`)
                        // 发送验证请求

                    } else {
                        // 验证失败！
                        return false
                    }
                })
            },
            handleFileChange(info) {
                // 上传文件处理
                if (info.file.status !== 'uploading') {
                    console.log(info.file, info.fileList)
                }
                if (info.file.status === 'done') {
                    this.$message.success(`${info.file.name} 上传成功`)
                } else if (info.file.status === 'error') {
                    this.$message.error(`${info.file.name} 上传失败`)
                }
            },
            resetHostForm() {
                // 重置添加主机的表单信息
                // this.$refs.hostRuleForm.resetFields()

            },
            resetHostCategoryForm() {
                // 重置添加主机类别的表单信息
                // this.$refs.hostCategoryRuleForm.resetFields()
            }
        }
    }
</script>

<style scoped>

</style>

