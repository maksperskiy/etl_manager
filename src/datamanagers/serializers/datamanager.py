from rest_framework import serializers

from ..models.datamanager import DataManager


class DataManagerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataManager
        fields = "__all__"


class DataManagerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataManager
        fields = ["pk", "name", "created_at", "author"]


class DataManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataManager
        fields = [
            "pk",
            "name",
            "datasource",
            "databuilder",
            "users_with_access",
        ]

    def validate(self, data):
        # if request := self.context.get("request"):
        #     data["author"] = request.user.pk
        return data
