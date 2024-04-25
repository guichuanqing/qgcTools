# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2023/11/23 10:42
# @File : forms.py
# Description : 文件说明
"""
from django import forms

class UploadXmindForm(forms.Form):
    xmind_file = forms.FileField()