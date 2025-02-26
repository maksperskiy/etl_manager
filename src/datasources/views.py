from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models.datasource import (
    DataSource,  # Replace with your actual model
    DataSourceType,
)
from .serializers import (
    DataSourceCommonConfigSerializer,
    DataSourceCreateSerializer,
    DataSourceDetailSerializer,
    DataSourceListSerializer,
)


class DataSourceListView(generics.ListAPIView):
    serializer_class = DataSourceListSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        if not request.user.is_superuser:
            query = Q(
                Q(author=request.user.pk)
                | Q(users_with_access__pk__contains=request.user.pk)
            )
            queryset = queryset.filter(query)
        return queryset.all()


class DataSourceCreateView(generics.CreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceCreateSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class DataSourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataSourceDetailSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        if not request.user.is_superuser:
            query = Q(
                Q(author=request.user.pk)
                | Q(users_with_access__pk__contains=request.user.pk)
            )
            queryset = queryset.filter(query)
        return queryset.all()


class DataSourceCommonConfigView(generics.ListAPIView):
    serializer_class = DataSourceCommonConfigSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        if not request.user.is_superuser:
            query = Q(
                Q(author=request.user.pk)
                | Q(users_with_access__pk__contains=request.user.pk)
            )
            queryset = queryset.filter(query)
        return queryset.all()

    def list(self, request, *args, **kwargs):
        source_type = self.kwargs.get("source_type")
        allowed_types = {
            "POSTGRES": ["host", "port", "database", "user", "password"],
            "MYSQL": ["host", "port", "database", "user", "password"],
            "S3": ["bucket", "access_key", "secret_key", "endpoint_url", "region_name"],
        }

        if not source_type in allowed_types:
            return Response(
                {
                    "error": f"source_type should by one of: {list(allowed_types.keys())}"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        queryset = self.get_queryset().filter(source_type=source_type)

        # Check if any records exist
        if not queryset.exists():
            return Response(
                {"error": "No records found"}, status=status.HTTP_404_NOT_FOUND
            )

        data = queryset.all()

        unique_configs = {
            tuple(
                {field: d.config[field] for field in allowed_types[source_type]}.items()
            )
            for d in data
        }
        unique_data = [dict(config=dict(t)) for t in unique_configs]

        serializer = self.get_serializer(unique_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
