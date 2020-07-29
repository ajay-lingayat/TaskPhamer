from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('find-account', views.find_account, name='find-account'),
    path('password-reset', views.password_reset, name='password-reset'),
]