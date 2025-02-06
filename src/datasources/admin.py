from django.contrib import admin
from .models import DataSource, DataSourceType
from django_json_widget.widgets import JSONEditorWidget
from django.db import models

from django import forms

class DataSourceForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = '__all__'
        widgets = {
            'config': JSONEditorWidget,
        }

    def clean_config(self):
        if self.cleaned_data['source_type'] == DataSourceType.S3:
            required = ['bucket', 'access_key', 'secret_key', 'endpoint_url']
            if not any(k in self.cleaned_data['config'] for k in required):
                raise forms.ValidationError("S3 config requires: bucket, access_key, secret_key, endpoint_url")
        return self.cleaned_data['config']

    def clean_upload(self):
        if self.cleaned_data['source_type'] == DataSourceType.FILE:
            if not self.cleaned_data['upload']:
                raise forms.ValidationError("FILE config requires: upload")
        return self.cleaned_data['upload']

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    form = DataSourceForm
    list_display = ('name', 'source_type', 'author', 'created_at', 'last_used')
    list_filter = ('source_type', 'author')
    readonly_fields = ('author', 'created_at', 'last_used')
    search_fields = ('name', 'author__username')
    filter_horizontal = ('users_with_access',)
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        if obj.source_type == DataSourceType.FILE and obj.upload:
            obj.config = obj.config or {}
            obj.config['path'] = obj.upload.url
        super().save_model(request, obj, form, change)
