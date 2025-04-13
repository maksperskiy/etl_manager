from django.urls import path

from datamanagers.views.datamanager import (DataManagerCreateView,
                                            DataManagerDetailView,
                                            DataManagerListView,
                                            DataManagerPerformRunView)

urlpatterns = [
    path("", DataManagerListView.as_view(), name="datamanager-list"),
    path("create/", DataManagerCreateView.as_view(), name="datamanager-create"),
    path(
        "<int:pk>/",
        DataManagerDetailView.as_view(),
        name="datamanager-detail",
    ),
    path(
        "<int:pk>/perform-run/",
        DataManagerPerformRunView.as_view(),
        name="datamanager-perform-run",
    ),
]
