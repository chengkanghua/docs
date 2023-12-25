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
    environment_name = serializers.CharField(source='environment.name', read_only=True)
    password = serializers.CharField(max_length=32, write_only=True, label="登录密码")

    class Meta:
        model = models.Host
        fields = ['id', 'category', "category_name", 'environment', "environment_name", 'name', 'ip_addr', 'port', 'description', 'username', 'password', "description"]

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

        if not password:
            return attrs

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

    def update(self, instance, validated_data):
        """更新主机信息"""
        name = validated_data.get("name", None)
        ip_addr = validated_data.get("ip_addr", None)
        port = validated_data.get("port", None)
        username = validated_data.get("username", None)
        description = validated_data.get("description", None)
        category = validated_data.get("category", None)
        password = validated_data.get("password", None)  # 此处，仅仅通过密码判断是否修改了主机信息，并不保存密码
        # 判断只有数据发生改动的字段从更新数据库信息
        if name and instance.name != name:
            instance.name = name
        if description and instance.description != description:
            instance.description = description
        if category and instance.category != category:
            instance.category = category
        if password:
            if ip_addr and instance.ip_addr != ip_addr:
                instance.ip_addr = ip_addr

            if port and instance.port != port:
                instance.port = port

            if username and instance.username != username:
                instance.username = username

        instance.save()
        return instance

