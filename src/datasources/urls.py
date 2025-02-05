from django.urls import path
from .views import DataSourceListView, DataSourceCreateView, DataSourceDetailView

urlpatterns = [
    path('datasources/', DataSourceListView.as_view(), name='datasource-list'),
    path('datasources/create/', DataSourceCreateView.as_view(), name='datasource-create'),
    path('datasources/<int:pk>/', DataSourceDetailView.as_view(), name='datasource-detail'),
]