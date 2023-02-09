from rest_framework import serializers
from . import models

from uric_api.utils.ssh import SSHParamiko
from uric_api.utils.key import PkeyManager
from django.conf import settings


class HostCategoryModelSeiralizer(serializers.ModelSerializer):
    """主机分类的序列化器"""

    class Meta:
        model = models.HostCategory
        fields = ['id', 'name']


class HostModelSerializers(serializers.ModelSerializer):
    """主机信息的序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    password = serializers.CharField(max_length=32, write_only=True, label="登录密码")

    class Meta:
        model = models.Host
        fields = ['id', 'category', "category_name", 'name', 'ip_addr', 'port', 'description', 'username', 'password']

    # def validate_username(self, value):
    #     if value == "root":
    #         return value
    #     else:
    #         raise serializers.ValidationError("访问用户是root用户！")

    def get_public_key(self):
        # todo 生成公私钥和管理主机的公私钥
        # 生成公私钥和管理主机的公私钥
        # 创建公私钥之前，我们先看看之前是否已经创建过公私钥了
        try:
            # 尝试从数据库中提取公私钥
            private_key, public_key = PkeyManager.get(settings.DEFAULT_KEY_NAME)
        except KeyError as e:
            # 没有公私钥存储到数据库中，则生成公私钥
            private_key, public_key = self.ssh.gen_key()
            # 将公钥和私钥保存到数据库中
            PkeyManager.set(settings.DEFAULT_KEY_NAME, private_key, public_key, 'ssh全局秘钥对')
        return public_key

    def validate(self, attrs):
        ip_addr = attrs.get('ip_addr')
        port = attrs.get('port')
        username = attrs.get('username')
        password = attrs.get('password')

        # todo 基于ssh验证主机信息是否正确
        self.ssh = SSHParamiko(ip_addr, port, username, password=str(password))

        self.client = self.ssh.get_connected_client()
        if self.client:  # 测试该链接是否能够使用
            public_key = self.get_public_key()
            # 上传公钥到服务器中
            self.ssh.upload_key(public_key)
            return attrs
        raise serializers.ValidationError("主机认证信息错误！")

    def create(self, validated_data):
        print('接受通过验证以后的数据字典:', validated_data)

        # todo 生成公私钥和管理主机的公私钥

        # 剔除密码字段，保存host记录
        password = validated_data.pop('password')
        instance = models.Host.objects.create(
            **validated_data
        )
        return instance
