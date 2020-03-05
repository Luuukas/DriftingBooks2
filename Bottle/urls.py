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

import Bottle.views as bottleviews

urlpatterns = [
    path('get_bottle_num/', bottleviews.get_bottle_num, name='get_bottle_num'),
    path('add_bottle/', bottleviews.add_bottle, name='add_bottle'),
    path('vis_bottle/', bottleviews.vis_bottle, name='vis_bottle'),
    path('get_bottle/', bottleviews.get_bottle, name='get_bottle'),
    path('pick_bottle_book/', bottleviews.pick_bottle_book, name='pick_bottle_book'),

]
