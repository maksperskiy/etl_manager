from django import forms
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from databuilders.models import DataBuilder, DataSample


@admin.register(DataSample)
class DataSampleAdmin(admin.ModelAdmin): ...


@admin.register(DataBuilder)
class DataBuilderAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "created_at")
    list_filter = ("author",)
    readonly_fields = ("author", "created_at")
    search_fields = (
        "name",
        "author__username",
    )
    filter_horizontal = ("users_with_access",)
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
