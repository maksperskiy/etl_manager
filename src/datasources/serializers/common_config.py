from rest_framework import serializers

from datasources.models import CommonDataSourceConfig


class CommonDataSourceConfigDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonDataSourceConfig
        fields = "__all__"


class CommonDataSourceConfigListSerializer(CommonDataSourceConfigDetailSerializer): ...


class CommonDataSourceConfigCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonDataSourceConfig
        fields = ["pk", "source_type", "config", "users_with_access"]

    def validate(self, data):
        # if request := self.context.get("request"):
        #     data["author"] = request.user.pk
        return data
