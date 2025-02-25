from django.urls import path

from .views import (DataSourceCommonConfigView, DataSourceCreateView,
                    DataSourceDetailView, DataSourceListView)

urlpatterns = [
    path("datasources/", DataSourceListView.as_view(), name="datasource-list"),
    path(
        "datasources/create/", DataSourceCreateView.as_view(), name="datasource-create"
    ),
    path(
        "datasources/<int:pk>/",
        DataSourceDetailView.as_view(),
        name="datasource-detail",
    ),
    path(
        "datasources/common/config/<str:source_type>/",
        DataSourceCommonConfigView.as_view(),
        name="datasource-common",
    ),
]
