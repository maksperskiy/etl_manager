from django.urls import path

from datasources.views.datasource import (
    DataSourceCreateView,
    DataSourceDetailView,
    DataSourceListView,
)

urlpatterns = [
    path("", DataSourceListView.as_view(), name="datasource-list"),
    path("create/", DataSourceCreateView.as_view(), name="datasource-create"),
    path(
        "<int:pk>/",
        DataSourceDetailView.as_view(),
        name="datasource-detail",
    )
]
