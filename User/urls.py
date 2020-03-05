"""driftingbooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

import User.views as userviews
from User.modifyInfo import sendSms2BindedPhone, changePassword, changePhonenumber

urlpatterns = [
    path('send_sms_view/', userviews.send_sms_view, name='send_sms_view'),
    path('register/', userviews.register, name='register'),
    path('login/', userviews.login, name='login'),
    path('get_user_infos/', userviews.get_user_infos, name='get_user_infos'),
    path('update_addresses/', userviews.update_addresses, name='update_addresses'),
    path('get_star_infos/', userviews.get_star_infos, name='get_star_infos'),
    path('add_star/', userviews.add_star, name='add_star'),
    path('del_star/', userviews.del_star, name='del_star'),
    path('get_public_key/', userviews.get_public_key, name='get_public_key'),
    path('send_sms_view2/', sendSms2BindedPhone, name='send_sms_view2'),
    path('change_password/', changePassword, name='change_password'),
    path('change_phonenumber/', changePhonenumber, name='change_phonenumber'),
]
