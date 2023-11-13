# -*- coding: utf-8 -*-
from django.urls import path, re_path
from .views import index_view, test_view

urlpatterns = [
    path('', index_view, name='index'),  # 主页，自然排序
    re_path(r'^test\.html$', test_view, name='test'),
    re_path(r'^', index_view, name='index'),
]