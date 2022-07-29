from django.contrib import admin
from django.urls import path

from info import views

urlpatterns = [
    path('import_info/', views.AddInfo.as_view(), name='info'),
    path('', views.index, name='index'),
]