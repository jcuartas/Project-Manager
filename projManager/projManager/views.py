#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:34:02 2017

@author: jcuartas
"""

from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def error_404(request):
    return render(request, 'error_404.html', {})