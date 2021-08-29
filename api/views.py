from django.shortcuts import render
from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status

from task_manager.models import Task, Checkpoint
from .serializers import TaskSerializer, CheckpointSerializer


class ActiveTaskList_(APIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({"tasks": serializer.data})


class TaskViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    # authentication_classes = (TokenAuthentication,)
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Task.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except AssertionError as e:
            return Response(None, status=status.HTTP_400_BAD_REQUEST,
                        headers=None)

        headers = self.get_success_headers(serializer.data)
        #return Response(serializer.data, status=status.HTTP_201_CREATED,
        #                headers=headers)

        return Response(None, status=status.HTTP_201_CREATED,
                        headers=headers)


class CheckpointViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    serializer_class = CheckpointSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Checkpoint.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except AssertionError as e:
            return Response(None, status=status.HTTP_400_BAD_REQUEST,
                        headers=None)

        headers = self.get_success_headers(serializer.data)
        #return Response(serializer.data, status=status.HTTP_201_CREATED,
        #                headers=headers)

        return Response(None, status=status.HTTP_201_CREATED,
                        headers=headers)
