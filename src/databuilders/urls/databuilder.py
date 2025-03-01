from django.urls import path

from databuilders.views.databuilder import (
    DataBuilderCreateView,
    DataBuilderDetailView,
    DataBuilderListView,
    DataBuilderTestView,
)

urlpatterns = [
    path("", DataBuilderListView.as_view(), name="databuilder-list"),
    path("create/", DataBuilderCreateView.as_view(), name="databuilder-create"),
    path(
        "<int:pk>/",
        DataBuilderDetailView.as_view(),
        name="databuilder-detail",
    ),
    path(
        "<int:pk>/test/",
        DataBuilderTestView.as_view(),
        name="databuilder-test",
    ),
]
