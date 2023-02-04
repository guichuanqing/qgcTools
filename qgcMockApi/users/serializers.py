# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2023/2/4 10:26
# @File : serializers.py
# Description : 文件说明
"""
from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer


# 创建序列化器
class UsersModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', 'is_active', 'last_login')