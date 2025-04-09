from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from databuilders.models import DataBuilder
from databuilders.serializers import (
    DataBuilderCreateSerializer,
    DataBuilderDetailSerializer,
    DataBuilderListSerializer,
)


class DataBuilderListView(generics.ListAPIView):
    serializer_class = DataBuilderListSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataBuilder.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class DataBuilderCreateView(generics.CreateAPIView):
    queryset = DataBuilder.objects.all()
    serializer_class = DataBuilderCreateSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class DataBuilderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataBuilderDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataBuilder.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class DataBuilderTestView(generics.RetrieveAPIView):
    serializer_class = DataBuilderDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataBuilder.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        result = instance.get_dataframe_head()

        return Response(result)
