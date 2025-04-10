from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models.datasource import (
    DataSource,  # Replace with your actual model
    DataSourceType,
)
from ..tasks import refresh_schema
from datasources.serializers import (
    DataSourceCreateSerializer,
    DataSourceDetailSerializer,
    DataSourceListSerializer,
)


class DataSourceListView(generics.ListAPIView):
    serializer_class = DataSourceListSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class DataSourceCreateView(generics.CreateAPIView):
    queryset = DataSource.objects.all()
    serializer_class = DataSourceCreateSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class DataSourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataSourceDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()

class DataSourceRefreshSchemaView(generics.RetrieveAPIView):
    serializer_class = DataSourceDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataSource.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        refresh_schema.delay(instance.pk)
        return Response({"details": "Schema refresh started"}, status=status.HTTP_200_OK)