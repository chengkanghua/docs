from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import ReleaseApp
from .serializers import ReleaseAppModelSerializer


class ReleaseAPIView(ModelViewSet):
    serializer_class = ReleaseAppModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ReleaseApp.objects
        app_name = self.request.query_params.get("app_name", None)
        description = self.request.query_params.get("description", None)
        tag = self.request.query_params.get("tag", None)
        if app_name:
            queryset = queryset.filter(name__contains=app_name)
        if description:
            queryset = queryset.filter(description__contains=description)
        if tag:
            queryset = queryset.filter(tag__contains=tag)

        return queryset.all()


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from uric_api.utils.gitlabapi import GitlabApi
from rest_framework.decorators import action

class GitlabAPIView(ViewSet):
    """gitlab仓库的管理"""
    git = GitlabApi()
    permission_classes = [IsAuthenticated]
    def list(self, request):
        """获取所有仓库列表"""
        return Response(self.git.get_projects())

    @action(methods=["GET"], detail=True)
    def branchs(self, request, pk):
        """获取指定项目的分支列表"""
        return Response(self.git.get_project_brances(pk))

    @action(methods=["GET"], detail=True)
    def commits(self, request, pk):
        """获取指定项目的commit历史版本"""
        return Response(self.git.get_project_commits(pk))

    def create(self, request):
        """创建仓库项目"""
        data = request.data
        result = self.git.create_project(data)
        return Response(result, status=status.HTTP_201_CREATED)


from uric_api.utils.jenkinsapi import Jenkinsapi
from rest_framework.decorators import action
from django.conf import settings


class JenkinsAPIView(ViewSet):
    """jenkins构建项目工程的管理"""
    permission_classes = [IsAuthenticated]
    jenkins = Jenkinsapi()
    def list(self, request):
        """获取job构建项目列表"""
        return Response(self.jenkins.get_jobs())

    @action(methods=["PUT"], detail=False)
    def build(self, request):
        """开始构建项目"""
        job_name = request.data.get("name")
        self.jenkins.build_job(job_name)
        job_info = self.jenkins.get_job_info(job_name)
        number = job_info["builds"][0]["number"]
        result = self.jenkins.get_build_info(job_name, number)
        return Response(result)

    def create(self, request):
        config_xml = f"""<?xml version='1.1' encoding='UTF-8'?>
        <project>
          <actions/>
          <description>{request.data.get('description')}</description>
          <keepDependencies>false</keepDependencies>
          <properties>
            <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.35">
              <gitLabConnection></gitLabConnection>
              <jobCredentialId></jobCredentialId>
              <useAlternativeCredential>false</useAlternativeCredential>
            </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
          </properties>
          <scm class="hudson.plugins.git.GitSCM" plugin="git@4.11.4">
            <configVersion>2</configVersion>
            <userRemoteConfigs>
              <hudson.plugins.git.UserRemoteConfig>
                <url>{request.data.get('git')}</url>
                <credentialsId>2d198778-f631-4425-b35d-0918a2c61554</credentialsId>
              </hudson.plugins.git.UserRemoteConfig>
            </userRemoteConfigs>
            <branches>
              <hudson.plugins.git.BranchSpec>
                <name>{request.data.get('branch')}</name>
              </hudson.plugins.git.BranchSpec>
            </branches>
            <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
            <submoduleCfg class="empty-list"/>
            <extensions/>
          </scm>
          <canRoam>true</canRoam>
          <disabled>false</disabled>
          <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
          <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
          <triggers>
            <hudson.triggers.SCMTrigger>
              <spec>{request.data.get('trigger')}</spec>
              <ignorePostCommitHooks>false</ignorePostCommitHooks>
            </hudson.triggers.SCMTrigger>
          </triggers>
          <concurrentBuild>false</concurrentBuild>
          <builders>
            <jenkins.plugins.publish__over__ssh.BapSshBuilderPlugin plugin="publish-over-ssh@1.24">
              <delegate>
                <consolePrefix>SSH: </consolePrefix>
                <delegate plugin="publish-over@0.22">
                  <publishers>
                    <jenkins.plugins.publish__over__ssh.BapSshPublisher plugin="publish-over-ssh@1.24">
                      <configName>{request.data.get('publishers')}</configName>
                      <verbose>false</verbose>
                      <transfers>
                        <jenkins.plugins.publish__over__ssh.BapSshTransfer>
                          <remoteDirectory>{request.data.get('remote_directory')}</remoteDirectory>
                          <sourceFiles>{request.data.get('source_files')}</sourceFiles>
                          <excludes></excludes>
                          <removePrefix>{request.data.get('remove_prefix')}</removePrefix>
                          <remoteDirectorySDF>false</remoteDirectorySDF>
                          <flatten>false</flatten>
                          <cleanRemote>false</cleanRemote>
                          <noDefaultExcludes>false</noDefaultExcludes>
                          <makeEmptyDirs>false</makeEmptyDirs>
                          <patternSeparator>[, ]+</patternSeparator>
                          <execCommand>{request.data.get('command')}</execCommand>
                          <execTimeout>120000</execTimeout>
                          <usePty>false</usePty>
                          <useAgentForwarding>false</useAgentForwarding>
                          <useSftpForExec>false</useSftpForExec>
                        </jenkins.plugins.publish__over__ssh.BapSshTransfer>
                      </transfers>
                      <useWorkspaceInPromotion>false</useWorkspaceInPromotion>
                      <usePromotionTimestamp>false</usePromotionTimestamp>
                    </jenkins.plugins.publish__over__ssh.BapSshPublisher>
                  </publishers>
                  <continueOnError>false</continueOnError>
                  <failOnError>false</failOnError>
                  <alwaysPublishFromMaster>false</alwaysPublishFromMaster>
                  <hostConfigurationAccess class="jenkins.plugins.publish_over_ssh.BapSshPublisherPlugin" reference="../.."/>
                </delegate>
              </delegate>
            </jenkins.plugins.publish__over__ssh.BapSshBuilderPlugin>
          </builders>
          <publishers/>
          <buildWrappers/>
        </project>
        """
        self.jenkins.create_job(request.data.get('job_name'), config_xml)
        return Response("ok", status=status.HTTP_201_CREATED)