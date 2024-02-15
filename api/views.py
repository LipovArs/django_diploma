from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from operator import add, sub

from board.models import Task
from .serializers import TaskSerializerListCreate, TaskAssing, TaskByStatusSerializer


@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.data.get('username'), password=request.data.get('password'))
    #       user.save()
            return Response({'message':'User created'}, status=201)
        except:
            return Response({'message':'Can`t create user'}, status=400)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=200)

    return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    

class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializerListCreate
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Task.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, status='1', assigner=None)


class TaskRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializerListCreate
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs['pk'])
    

    def perform_update(self, serializer):
        if serializer.instance.creator == self.request.user or self.request.user.is_superuser:
            serializer.save()
        else:
            raise ValidationError('You don`t have permision')
    

class BecomeAssigner(generics.UpdateAPIView):

    serializer_class = TaskAssing
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        
        if serializer.instance.assigner == None and self.request.user == serializer.instance.creator:
            serializer.instance.assigner = self.request.user
            serializer.save()
        else:
            raise ValidationError('You allready assigner')
        

class TaskMove(generics.UpdateAPIView):

    serializer_class = TaskAssing
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs['pk'])
    

    def change_satus_help(self, task, operator):
        task.status = operator(int(task.status), 1)
        task.assigner = None
        return task


    def perform_update(self, serializer):
        task = serializer.instance
        if self.request.user.is_superuser:
            if self.kwargs['direction'] == 'right' and int(task.status) == 4:
                task = self.change_satus_help(task, add)
            elif self.kwargs['direction'] == 'left'and int(task.status) == 5:
                task = self.change_satus_help(task, sub)
            else:
                raise ValidationError('Can`t move task to that direction')
            task.save()
        elif serializer.instance.assigner == self.request.user:
            if self.kwargs['direction'] == 'right' and int(task.status) < 4:
                task = self.change_satus_help(task, add)
            elif self.kwargs['direction'] == 'left'and int(task.status) > 1:
                task = self.change_satus_help(task, sub)
            else:
                raise ValidationError('Can`t move task to that direction')
            task.save()
        else:
            raise ValidationError('You are not assigned to this task')
        

class TaskByStatus(generics.ListAPIView):
    serializer_class = TaskByStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(status=self.kwargs['status_id'])
    

class TaskDelete(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerListCreate
    permission_classes =[permissions.IsAdminUser]


class AppointAssigner(generics.UpdateAPIView):

    serializer_class = TaskAssing
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Task.objects.filter(pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        
        serializer.instance.assigner = User.objects.get(pk=self.kwargs['user_id'])
        serializer.save()