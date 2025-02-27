from django.urls import path

from .views import (DataSourceCommonConfigView, DataSourceCreateView,
                    DataSourceDetailView, DataSourceListView)

urlpatterns = [
    path("", DataSourceListView.as_view(), name="datasource-list"),
    path(
        "create/", DataSourceCreateView.as_view(), name="datasource-create"
    ),
    path(
        "<int:pk>/",
        DataSourceDetailView.as_view(),
        name="datasource-detail",
    ),
    path(
        "common/config/<str:source_type>/",
        DataSourceCommonConfigView.as_view(),
        name="datasource-common",
    ),
]
