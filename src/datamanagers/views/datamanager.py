from django.db.models import Q
from rest_framework import generics, status
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from datamanagers.models import DataManager
from datamanagers.serializers import (DataManagerCreateSerializer,
                                      DataManagerDetailSerializer,
                                      DataManagerListSerializer)
from datamanagers.tasks import run_process


class DataManagerListView(generics.ListAPIView):
    serializer_class = DataManagerListSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataManager.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class DataManagerCreateView(generics.CreateAPIView):
    queryset = DataManager.objects.all()
    serializer_class = DataManagerCreateSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]


class DataManagerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataManagerDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataManager.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()


class DataManagerPerformRunView(generics.RetrieveAPIView):
    serializer_class = DataManagerDetailSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        request = self.request
        queryset = DataManager.objects.all()
        # if not request.user.is_superuser:
        #     query = Q(
        #         Q(author=request.user.pk)
        #         | Q(users_with_access__pk__contains=request.user.pk)
        #     )
        #     queryset = queryset.filter(query)
        return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        run_process.delay(instance.pk)
        return Response({"details": "Run started"}, status=status.HTTP_200_OK)
