#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Time : 2020/9/8 22:22
# @Author : Yulong Sun
# @Site : 
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from .views import  *
urlpatterns=[
    path('zhuce',zhuce)
]