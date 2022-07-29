from django.contrib import admin
from django.urls import path

from ads import views

urlpatterns = [
    path('', views.index),
    path('ad/', views.AdListView.as_view(), name='ads'),
    path("ad/<int:pk>/", views.AdDetailView.as_view(), name='ad'),
    path("ad/create/", views.AdCreateView.as_view(), name='create_ad'),
    path("ad/<int:pk>/update/", views.AdUpdateView.as_view(), name='update_ad'),
    path("ad/<int:pk>/upload_image/", views.AdImageView.as_view(), name='upload_image'),
    path("ad/<int:pk>/delete/", views.AdDeleteView.as_view(), name='delete_ad'),
    path('cat/', views.CatListView.as_view(), name='cats'),
    path("cat/<int:pk>/", views.CatDetailView.as_view(), name='cat'),
    path("cat/create/", views.CatCreateView.as_view(), name='create_cat'),
    path("cat/<int:pk>/update/", views.CatUpdateView.as_view(), name='update_cat'),
    path("cat/<int:pk>/delete/", views.CatDeleteView.as_view(), name='delete_cat'),
]
