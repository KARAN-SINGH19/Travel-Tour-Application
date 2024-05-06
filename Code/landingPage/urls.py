from django.contrib import admin
from django.urls import path, include
from landingPage import views
app_name = 'landingPage'

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('login_user/', views.login_user, name='login_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('verifyUser/', views.verifyUser, name='verifyUser'),
    path('change_password/', views.change_password, name='change_password'),
]
