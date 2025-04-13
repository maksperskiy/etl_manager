from django import forms
from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from datamanagers.models import DataManager, ManagerRunPeriodicTask


class ManagerRunPeriodicTaskInline(admin.TabularInline):
    model = ManagerRunPeriodicTask
    tab = True
    fields = (
        "interval",
        "crontab",
        "enabled",
    )


@admin.register(DataManager)
class DataManagerAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "created_at", "last_status", "last_checked")
    inlines = [ManagerRunPeriodicTaskInline]

    list_filter = ("author",)
    readonly_fields = ("author", "created_at", "last_status", "last_checked")
    search_fields = (
        "name",
        "author__username",
    )
    filter_horizontal = ("users_with_access",)

    def last_run_status(self, obj):
        # latest_manager_run = ManagerRun.objects.filter(datamanager=obj).order_by("-created_at").first()
        # return latest_manager_run.status if latest_manager_run else "No manager runs"
        return "status_placeholder"

    def last_run(self, obj):
        # latest_manager_run = ManagerRun.objects.filter(datamanager=obj).order_by("-created_at").first()
        # return latest_manager_run.created_at if latest_manager_run else "No manager runs"
        return "placeholder"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
