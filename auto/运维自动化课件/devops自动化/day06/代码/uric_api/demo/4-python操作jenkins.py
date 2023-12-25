import jenkins


class Jenkinsapi(object):
    def __init__(self, url, user, token):
        self.server_url = url
        self.user = user
        self.token = token
        self.conn = jenkins.Jenkins(self.server_url, username=self.user, password=self.token)

    def get_jobs(self):
        """
        获取所有的构建项目列表
        :return:
        """
        return self.conn.get_jobs()

    def get_job_info(self, job):
        """
        根据项目名获取构建项目
        :param job:
        :return:
        """
        return self.conn.get_job_info(job)

    def build_job(self,job,**kwargs):
        """
        开始构建项目
        :param job:
        :param kwargs:
        :return:
        """
        # dict1 = {"version":11} # 参数话构建
        # dict2 = {'Status': 'Rollback', 'BUILD_ID': '26'} # 回滚
        return self.conn.build_job(job, parameters=kwargs)

    def get_build_info(self,job, build_number):
        """
        通过构建编号获取构建项目的构建记录
        :param job:
        :param build_number:
        :return:
        """
        return self.conn.get_build_info(job,build_number)

    def get_job_config(self, job):
        '''
        获取xml文件
        '''
        res = self.conn.get_job_config(job)
        print(res)

    def create_job(self,name, config_xml):
        '''
        任务名字
        xml格式的字符串
        '''
        self.conn.create_job(name, config_xml)

    def update_job(self,name, config_xml):
        res = self.conn.reconfig_job(name,config_xml)
        print(res)

    def get(self):
        res = self.conn.list_credentials("/taobaotest4/descriptorByName/hudson.plugins.git.UserRemoteConfig")
        print(res)

if __name__ == '__main__':
    server_url = 'http://192.168.101.8:8888/'
    username = 'admin'
    password = '11217915472cb72a7edb9a4de8113a5928'
    server = Jenkinsapi(server_url, username, password)

    # jobs = server.get_jobs()
    # print(jobs)

    # job = server.get_job_info("project-1")
    # print(job)

    # build_number = server.build_job("project-1")
    # print(build_number)

    # info = server.get_build_info("project-1", 2)
    # print(info)

    # # 先获取已有构建项目的配置文档
    # config_xml = server.get_job_config("taobaotest1")
    # print(config_xml)

    # 获取票据
    server.get()

#     config_xml = """<?xml version='1.1' encoding='UTF-8'?>
# <project>
#   <actions/>
#   <description>测试代码发布</description>
#   <keepDependencies>false</keepDependencies>
#   <properties>
#     <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.35">
#       <gitLabConnection></gitLabConnection>
#       <jobCredentialId></jobCredentialId>
#       <useAlternativeCredential>false</useAlternativeCredential>
#     </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
#   </properties>
#   <scm class="hudson.plugins.git.GitSCM" plugin="git@4.11.4">
#     <configVersion>2</configVersion>
#     <userRemoteConfigs>
#       <hudson.plugins.git.UserRemoteConfig>
#         <url>http://192.168.101.8:8993/root/taobao.git</url>
#         <credentialsId>2d198778-f631-4425-b35d-0918a2c61554</credentialsId>
#       </hudson.plugins.git.UserRemoteConfig>
#     </userRemoteConfigs>
#     <branches>
#       <hudson.plugins.git.BranchSpec>
#         <name>*/master</name>
#       </hudson.plugins.git.BranchSpec>
#     </branches>
#     <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
#     <submoduleCfg class="empty-list"/>
#     <extensions/>
#   </scm>
#   <canRoam>true</canRoam>
#   <disabled>false</disabled>
#   <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
#   <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
#   <triggers>
#     <hudson.triggers.SCMTrigger>
#       <spec>*/1 * * * *</spec>
#       <ignorePostCommitHooks>false</ignorePostCommitHooks>
#     </hudson.triggers.SCMTrigger>
#   </triggers>
#   <concurrentBuild>false</concurrentBuild>
#   <builders>
#     <jenkins.plugins.publish__over__ssh.BapSshBuilderPlugin plugin="publish-over-ssh@1.24">
#       <delegate>
#         <consolePrefix>SSH: </consolePrefix>
#         <delegate plugin="publish-over@0.22">
#           <publishers>
#             <jenkins.plugins.publish__over__ssh.BapSshPublisher plugin="publish-over-ssh@1.24">
#               <configName>u192.168.233.136</configName>
#               <verbose>true</verbose>
#               <transfers>
#                 <jenkins.plugins.publish__over__ssh.BapSshTransfer>
#                   <remoteDirectory>Desktop/proj/taobao</remoteDirectory>
#                   <sourceFiles>*,taobao/*.*</sourceFiles>
#                   <excludes></excludes>
#                   <removePrefix></removePrefix>
#                   <remoteDirectorySDF>false</remoteDirectorySDF>
#                   <flatten>false</flatten>
#                   <cleanRemote>false</cleanRemote>
#                   <noDefaultExcludes>false</noDefaultExcludes>
#                   <makeEmptyDirs>false</makeEmptyDirs>
#                   <patternSeparator>[, ]+</patternSeparator>
#                   <execCommand>cd /home/docker/Desktop/proj/taobao
# pip install -r requirements.txt
# kill -9 $(ps -aef | grep uwsgi | grep -v grep | awk &apos;{print $2}&apos;)
# /home/docker/.local/bin/uwsgi --ini ./uwsgi.ini</execCommand>
#                   <execTimeout>120000</execTimeout>
#                   <usePty>false</usePty>
#                   <useAgentForwarding>false</useAgentForwarding>
#                   <useSftpForExec>false</useSftpForExec>
#                 </jenkins.plugins.publish__over__ssh.BapSshTransfer>
#               </transfers>
#               <useWorkspaceInPromotion>false</useWorkspaceInPromotion>
#               <usePromotionTimestamp>false</usePromotionTimestamp>
#             </jenkins.plugins.publish__over__ssh.BapSshPublisher>
#             <jenkins.plugins.publish__over__ssh.BapSshPublisher plugin="publish-over-ssh@1.24">
#               <configName>u192.168.233.136</configName>
#               <verbose>false</verbose>
#               <transfers>
#                 <jenkins.plugins.publish__over__ssh.BapSshTransfer>
#                   <remoteDirectory>Desktop/proj/demo</remoteDirectory>
#                   <sourceFiles>*,taobao/*.*</sourceFiles>
#                   <excludes></excludes>
#                   <removePrefix></removePrefix>
#                   <remoteDirectorySDF>false</remoteDirectorySDF>
#                   <flatten>false</flatten>
#                   <cleanRemote>false</cleanRemote>
#                   <noDefaultExcludes>false</noDefaultExcludes>
#                   <makeEmptyDirs>false</makeEmptyDirs>
#                   <patternSeparator>[, ]+</patternSeparator>
#                   <execCommand>pwd</execCommand>
#                   <execTimeout>120000</execTimeout>
#                   <usePty>false</usePty>
#                   <useAgentForwarding>false</useAgentForwarding>
#                   <useSftpForExec>false</useSftpForExec>
#                 </jenkins.plugins.publish__over__ssh.BapSshTransfer>
#               </transfers>
#               <useWorkspaceInPromotion>false</useWorkspaceInPromotion>
#               <usePromotionTimestamp>false</usePromotionTimestamp>
#             </jenkins.plugins.publish__over__ssh.BapSshPublisher>
#           </publishers>
#           <continueOnError>false</continueOnError>
#           <failOnError>false</failOnError>
#           <alwaysPublishFromMaster>false</alwaysPublishFromMaster>
#           <hostConfigurationAccess class="jenkins.plugins.publish_over_ssh.BapSshPublisherPlugin" reference="../.."/>
#         </delegate>
#       </delegate>
#     </jenkins.plugins.publish__over__ssh.BapSshBuilderPlugin>
#   </builders>
#   <publishers/>
#   <buildWrappers/>
# </project>
# """
#     server.create_job("project-2", config_xml=config_xml)
