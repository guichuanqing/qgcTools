# -*- coding: utf-8 -*-
from django.urls import path, re_path
from .views import index_view, upload_xmind

urlpatterns = [
    re_path(r'^upload\.html$', upload_xmind, name='upload_xmind'),
    # path('', index_view, name='index'),  # 主页，自然排序
    re_path(r'^', index_view, name='index'),
]