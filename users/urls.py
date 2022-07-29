from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path('', views.index),
    path('user/', views.UserListView.as_view(), name='users'),
    path("user/<int:pk>/", views.UserDetailView.as_view(), name='user'),
    path("user/create/", views.UserCreateView.as_view(), name='create_user'),
    path("user/<int:pk>/update/", views.UserUpdateView.as_view(), name='update_user'),
    path("user/<int:pk>/delete/", views.UserDeleteView.as_view(), name='delete_user'),
]
