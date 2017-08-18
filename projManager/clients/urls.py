#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 18:00:15 2017

@author: jcuartas
"""

from django.conf.urls import url
from clients.views import ShowClass
from clients.views import LoginClass
from clients.views import logout
from clients.views import DashboardClass
from clients.views import CreateClass
from clients.views import EditClass
from clients.views import edit_password
from clients.views import edit_client

app_name = 'client'

urlpatterns = [
#    url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),    
    url(r'^show/(?P<username_url>\w+)/$', ShowClass.as_view(), name = 'show'),
    url(r'^login/$', LoginClass.as_view(), name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^dashboard/$', DashboardClass.as_view(), name = 'dashboard'),
    url(r'^create/$', CreateClass.as_view(), name = 'create'),
    url(r'^edit/$', EditClass.as_view(), name = 'edit'),
    url(r'^edit_password/$', edit_password, name = 'edit_password'),
    url(r'^edit_client/$', edit_client, name = 'edit_client'),          
]