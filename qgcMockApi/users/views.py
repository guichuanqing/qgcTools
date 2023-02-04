from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import UsersModelSerializer

# 定义视图集
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersModelSerializer
