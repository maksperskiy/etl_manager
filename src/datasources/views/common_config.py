from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from datasources.models import CommonDataSourceConfig
from datasources.serializers import (
    CommonDataSourceConfigCreateSerializer,
    CommonDataSourceConfigDetailSerializer,
    CommonDataSourceConfigListSerializer,
)


class CommonDataSourceConfigListView(generics.ListAPIView):
    serializer_class = CommonDataSourceConfigListSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = CommonDataSourceConfig.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class CommonDataSourceConfigCreateView(generics.CreateAPIView):
    queryset = CommonDataSourceConfig.objects.all()
    serializer_class = CommonDataSourceConfigCreateSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class CommonDataSourceConfigDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommonDataSourceConfigDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = CommonDataSourceConfig.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()
