"""tic_tac_toe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    # path('progress2/', views.progress2, name='progress2'),
    # path('getCellId/', views.getCellId, name='getCellId'),
    # path('showModels/', views.showModels, name='showModels'),
    path('', views.index, name='index'),
    path('session/', views.session, name='session'),
    path('make_move/', views.make_move, name='make_move'),
    path('getNextPlayer/', views.getNextPlayer, name='getNextPlayer'),
    path('getCellIds/', views.getCellIds, name='getCellIds'),
    path('gg/', views.gg, name='gg'),
    path('admin/', admin.site.urls)
]
