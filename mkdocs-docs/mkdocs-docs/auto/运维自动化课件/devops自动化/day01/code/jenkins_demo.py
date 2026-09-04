import jenkins

if __name__ == '__main__':
    """连接jenkins"""
    # 基于登陆密码连接jenkins
    # server = jenkins.Jenkins('http://192.168.101.8:8888/', username='admin', password='7bb3d493057242edaf5a9e72c63ca27e')
    # 基于token连接jenkins
    server = jenkins.Jenkins('http://10.211.55.20:8888/', username='kanghua', password='1134c952f271ee074c74e96832ead64d28')
    # print(server)

    # """我是谁?"""
    # user = server.get_whoami()
    # print(user)
    #
    # """jenkins的版本号"""
    # version = server.get_version()
    # print(version)  # 2.361.1

    # """查看所有的构建任务"""
    # jobs = server.get_jobs()
    # print(jobs)
    # """
    # [{
    #     '_class': 'hudson.model.FreeStyleProject',   # 构建项目的类型  FreeStyleProject 表示自由风格的构建项目
    #     'name': 'demo',                              # 构建项目的名称
    #     'url': 'http://192.168.101.8:8888/job/demo/',   # 访问地址
    #     'color': 'notbuilt',                            # 构建状态  【notbuilt, blue, 】
    #     'fullname': 'demo'                              # 构建项目的名称
    # }]
    # """

    # """获取指定的构建任务信息"""
    # info = server.get_job_info(name="demo")
    # print(info)
    # """
    # {
    #     '_class': 'hudson.model.FreeStyleProject',   # 构建项目类型
    #     'actions': [   # 构建项目的配置配置
    #         {},
    #         {},
    #         {'_class': 'org.jenkinsci.plugins.displayurlapi.actions.JobDisplayAction'},
    #         {'_class': 'com.cloudbees.plugins.credentials.ViewCredentialsAction'}
    #     ],
    #     'description': '测试构建项目',   # 构建项目的描述
    #     'displayName': 'demo',         # 构建项目的名称
    #     'displayNameOrNull': None,
    #     'fullDisplayName': 'demo',
    #     'fullName': 'demo',
    #     'name': 'demo',                # 构建项目的名称
    #     'url': 'http://192.168.101.8:8888/job/demo/',    # 访问地址
    #     'buildable': True,                               # 当前构建项目是否属于可构建状态（激活状态）
    #     'builds': [{                                     # 构建项目的执行记录
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'
    #     }],
    #     'color': 'blue',                                 # 构建项目的执行状态（晴雨表）
    #     'firstBuild': {                                  # 首次构建的结果
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'
    #     },
    #     'healthReport': [{                               # 构建项目的健康报告（晴雨表）
    #         'description': 'Build stability: No recent builds failed.',
    #         'iconClassName': 'icon-health-80plus',
    #         'iconUrl': 'health-80plus.png',
    #         'score': 100                                 # 构建任务的成功率
    #     }],
    #     'inQueue': False,                                # 是否处理队列等待中
    #     'keepDependencies': False,
    #     'lastBuild': {                                   # 上一次构建构建任务的状态
    #         '_class': 'hudson.model.FreeStyleBuild',
    #         'number': 1,
    #         'url': 'http://192.168.101.8:8888/job/demo/1/'},
    #         'lastCompletedBuild': {                     # 上一次完成构建的执行记录
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastFailedBuild': None,                    # 上一次失败记录
    #         'lastStableBuild': {                        # 上次构建状态
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastSuccessfulBuild': {                    # 上一次成功记录
    #             '_class': 'hudson.model.FreeStyleBuild',
    #             'number': 1,
    #             'url': 'http://192.168.101.8:8888/job/demo/1/'
    #         },
    #         'lastUnstableBuild': None,
    #         'lastUnsuccessfulBuild': None,
    #         'nextBuildNumber': 2,
    #         'property': [],
    #         'queueItem': None,
    #         'concurrentBuild': False,
    #         'disabled': False,
    #         'downstreamProjects': [],
    #         'labelExpression': None,
    #         'scm': {'_class': 'hudson.scm.NullSCM'},
    #         'upstreamProjects': []
    #     }
    # """

    # """开始构建任务"""
    # 如果要构建的任务，不存在，则报错！！
    # build_id = server.build_job(name='demo')
    # print(build_id)

    # """设置构建任务为禁用状态(不可构建状态)"""
    # server.disable_job(name='demo')

    # """设置构建任务为激活激活状态(可构建状态)"""
    # server.enable_job(name="demo")

    # """删除一个构建任务"""
    # server.delete_job(name='demo')

    # """获取项目的最后一次构建编号"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # print(last_build_number)

    # """根据构建编号来获取构建结果"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_info('demo', last_build_number)['result']
    # print(result)  # SUCCESS

    # """根据构建编号获取构建过程中的终端输出内容"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_console_output(name='demo', number=last_build_number)
    # print(result)

    # """根据构建编号获取构建的测试报告【Allure】"""
    # last_build_number = server.get_job_info('demo')['lastBuild']['number']
    # result = server.get_build_test_report(name='demo', number=last_build_number)
    # print(result)

    """基于已有的任务，生成一份xml配置文档"""
    # config_xml = server.get_job_config(name="demo")
    # print(config_xml)

    #     """
    #     基于xml构建项目
    #     """
    #     config_xml = """<project>
    # <description>测试构建项目</description>
    # <keepDependencies>false</keepDependencies>
    # <properties/>
    # <scm class="hudson.scm.NullSCM"/>
    # <canRoam>true</canRoam>
    # <disabled>false</disabled>
    # <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
    # <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
    # <triggers/>
    # <concurrentBuild>false</concurrentBuild>
    # <builders>
    # <hudson.tasks.Shell>
    #   <command>echo "hello, project-1"</command>
    #   <configuredLocalRules/>
    # </hudson.tasks.Shell>
    # </builders>
    # <publishers/>
    # <buildWrappers/>
    # </project>"""
    #
    #     server.create_job("project-1", config_xml=config_xml)

