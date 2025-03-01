from rest_framework import serializers

from ..models.databuilder import DataBuilder


class DataBuilderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBuilder
        fields = "__all__"


class DataBuilderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBuilder
        fields = ["pk", "name", "created_at", "author"]


class DataBuilderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataBuilder
        fields = [
            "pk",
            "name",
            "config",
            "datasources",
            "databuilders",
            "users_with_access",
        ]

    def validate(self, data):
        # if request := self.context.get("request"):
        #     data["author"] = request.user.pk
        return data
