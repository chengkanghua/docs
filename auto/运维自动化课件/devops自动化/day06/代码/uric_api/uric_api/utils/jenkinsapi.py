import jenkins
from django.conf import settings


class Jenkinsapi(object):
    def __init__(self, server_url=None, username=None, password=None):
        self.server_url = settings.JENKINS['server_url'] if server_url is None else server_url
        self.username = settings.JENKINS['username'] if username is None else username
        self.password = settings.JENKINS['password'] if password is None else password
        self.conn = jenkins.Jenkins(url=self.server_url, username=self.username, password=self.password)

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

    def build_job(self,job, **kwargs):
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

    def get_job_config(self,job):
        '''
        获取xml文件
        '''
        return self.conn.get_job_config(job)

    def create_job(self,name,config_xml):
        '''
        任务名字
        xml格式的字符串
        '''
        return self.conn.create_job(name, config_xml)

    def update_job(self,name,config_xml):
        res = self.conn.reconfig_job(name,config_xml)
        return res

