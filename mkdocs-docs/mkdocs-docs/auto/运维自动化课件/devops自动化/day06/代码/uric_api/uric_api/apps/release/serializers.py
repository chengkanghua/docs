from rest_framework import serializers
from .models import ReleaseApp


class ReleaseAppModelSerializer(serializers.ModelSerializer):
    """发布应用的序列化器"""
    class Meta:
        model = ReleaseApp
        fields = ["id", "name", "tag", "description"]

    def create(self, validated_data):
        """添加"""
        print("self.context", self.context)
        # self.context = {"request": request, "view": view, "format": format}
        validated_data["user_id"] = self.context["request"].user.id
        return super().create(validated_data)
