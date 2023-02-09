from rest_framework import serializers
from . import models

from uric_api.utils.ssh import SSHParamiko


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

    def validate_username(self, value):
        if value == "root":
            return value
        else:
            raise serializers.ValidationError("访问用户是root用户！")

    def validate(self, attrs):
        ip_addr = attrs.get('ip_addr')
        port = attrs.get('port')
        username = attrs.get('username')
        password = attrs.get('password')

        # todo 基于ssh验证主机信息是否正确

        cli = SSHParamiko(ip_addr, port, username, password=str(password))
        if cli.is_validated():  # 测试该链接是否能够使用
            return attrs
        raise serializers.ValidationError("主机认证失败，用户或密码错误！")

    def create(self, validated_data):
        print('接受通过验证以后的数据字典:', validated_data)

        # todo 生成公私钥和管理主机的公私钥

        # 剔除密码字段，保存host记录
        password = validated_data.pop('password')
        instance = models.Host.objects.create(
            **validated_data
        )
        return instance
