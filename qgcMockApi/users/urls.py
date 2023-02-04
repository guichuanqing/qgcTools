# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2023/2/4 10:32
# @File : urls.py
# Description : 文件说明
"""

from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

# 创建DefaultRouter对象
router = DefaultRouter()
# 批量添加路由
router.register(r'users', UsersViewSet)

urlpatterns = [

]

urlpatterns += router.urls