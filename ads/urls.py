from django.contrib import admin
from django.urls import path

from ads import views

urlpatterns = [
    path('', views.index),
    path('ad/', views.AdListView.as_view()),
    path("ad/<int:pk>/", views.AdDetailView.as_view()),
    path("ad/create/", views.AdCreateView.as_view()),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view()),
    path("ad/image/<int:pk>/", views.AdImageView.as_view()),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view()),
    path('cat/', views.CatListView.as_view()),
    path("cat/<int:pk>/", views.CatDetailView.as_view()),
    path("cat/create/", views.CatCreateView.as_view()),
    path("cat/<int:pk>/update/", views.CatUpdateView.as_view()),
    path("cat/<int:pk>/delete/", views.CatDeleteView.as_view()),
]
