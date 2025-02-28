from rest_framework import serializers

from ..models.datasource import DataSource


class DataSourceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = "__all__"

    file_ext = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()

    def get_file_ext(self, obj: DataSource):
        return obj.upload.name.rsplit(".")[-1] if obj.source_type == "FILE" else None

    def get_file_name(self, obj: DataSource):
        return obj.upload.name.rsplit("/")[-1] if obj.source_type == "FILE" else None


class DataSourceListSerializer(DataSourceDetailSerializer):
    class Meta:
        model = DataSource
        fields = [
            "pk",
            "name",
            "source_type",
            "author",
            "created_at",
            "last_used",
            "file_ext",
            "file_name",
        ]


class DataSourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ["pk", "name", "source_type", "config", "upload", "users_with_access"]

    def validate(self, data):
        if data["source_type"] == "FILE" and not data.get("upload"):
            raise serializers.ValidationError(
                "File should be uploaded for 'FILE' source_type."
            )
        if data.get("upload") and not data["source_type"] == "FILE":
            raise serializers.ValidationError(
                "File can be uploaded only for 'FILE' source_type."
            )
        if file := data.get("upload"):
            if file.size > 50 * 1024 * 1024:
                raise serializers.ValidationError("File size cannot exceed 50MB.")
            if not any(
                [
                    file.name.endswith(f".{ext}")
                    for ext in ["xlsx", "xls", "csv", "json"]
                ]
            ):
                raise serializers.ValidationError("File is not supported.")
            
        # if request := self.context.get("request"):
        #     data["author"] = request.user.pk
        return data
