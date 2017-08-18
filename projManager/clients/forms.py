#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 19:26:21 2017

@author: jcuartas
"""

from django import forms
from django.contrib.auth.models import User

"""
Constants
"""

ERROR_MESSAGE_USER = {'required': 'El username es requerido', 'unique':'El usuario ya se encuentra registrado', 'invalid':'El username es incorrecto'}
ERROR_MESSAGE_PASSWORD = {'required': 'El password es requerido'}
ERROR_MESSAGE_EMAIL = {'required': 'El email es requerido', 'invalid':'Ingrese un correo valido'}


"""
Functions
"""
def must_be_gt(value_password):
    if len(value_password) < 5:
        raise forms.ValidationError('El password debe contener por lo menos 5 caracteres, desde una func')

"""
Class
"""

class LoginUserForm(forms.Form):
    username = forms.CharField( max_length = 20)
    password = forms.CharField( max_length = 20, widget = forms.PasswordInput() )
    
    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update( {'class':'username_login'} )
        self.fields['username'].widget.attrs.update( {'class':'password_login'} )
    
class CreateUserForm(forms.ModelForm):
    username = forms.CharField( max_length = 20, error_messages = ERROR_MESSAGE_USER)
    password = forms.CharField( max_length = 20, widget = forms.PasswordInput(), error_messages = ERROR_MESSAGE_PASSWORD)
    email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class EditUserForm(forms.ModelForm):
    username = forms.CharField( max_length = 20, error_messages = ERROR_MESSAGE_USER)
    email = forms.CharField(error_messages = ERROR_MESSAGE_EMAIL)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class EditPasswordForm(forms.Form):
    password = forms.CharField( max_length = 20, widget = forms.PasswordInput() )
    new_password = forms.CharField( max_length = 20, widget = forms.PasswordInput(), validators = [must_be_gt] )
    repeat_password = forms.CharField( max_length = 20, widget = forms.PasswordInput(), validators = [must_be_gt] )
    
    def clean(self):
        clean_data = super(EditPasswordForm, self).clean()

        if 'new_password' in clean_data.keys():
            password1 = clean_data['new_password']
        else:
            password1 = ''
        if 'repeat_password' in clean_data.keys():
            password2 = clean_data['repeat_password']
        else:
            password2 = ''
        if password1 == '' or password2 == '':
            raise forms.ValidationError('Nuevo pasword inválido')
        if password1 != password2:
            raise forms.ValidationError('Los password no son los mismos')
    