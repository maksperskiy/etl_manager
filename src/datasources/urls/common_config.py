from django.urls import path

from datasources.views.common_config import (
    CommonDataSourceConfigCreateView,
    CommonDataSourceConfigDetailView,
    CommonDataSourceConfigListView,
)

urlpatterns = [
    path("", CommonDataSourceConfigListView.as_view(), name="datasource-list"),
    path(
        "create/", CommonDataSourceConfigCreateView.as_view(), name="datasource-create"
    ),
    path(
        "<int:pk>/",
        CommonDataSourceConfigDetailView.as_view(),
        name="datasource-detail",
    ),
]
