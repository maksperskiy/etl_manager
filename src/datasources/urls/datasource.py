from django.urls import path

from datasources.views.datasource import (
    DataSourceCreateView,
    DataSourceDetailView,
    DataSourceListView,
    DataSourceRefreshSchemaView,
)

urlpatterns = [
    path("", DataSourceListView.as_view(), name="datasource-list"),
    path("create/", DataSourceCreateView.as_view(), name="datasource-create"),
    path(
        "<int:pk>/",
        DataSourceDetailView.as_view(),
        name="datasource-detail",
    ),
    path(
        "<int:pk>/refresh-schema/",
        DataSourceRefreshSchemaView.as_view(),
        name="datasource-refresh-schema",
    ),
]
