from rest_framework import generics
from .models import DataSource  # Replace with your actual model
from .serializers import DataSourceListSerializer, DataSourceDetailSerializer, DataSourceCreateSerializer

class DataSourceListView(generics.ListAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceListSerializer

class DataSourceCreateView(generics.CreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceCreateSerializer

class DataSourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceDetailSerializer