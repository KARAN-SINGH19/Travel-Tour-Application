from django.contrib import admin
from django.urls import path, include
from home import views
app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('hotelHome/', views.hotelHome, name='hotelHome'),
    path('hotels/', views.hotels, name='hotels'),
    path('hotelSearch/', views.hotelSearch, name='hotelSearch'),
    path('resortHome/', views.resortHome, name='resortHome'),
    path('resorts/', views.resorts, name='resorts'),
    path('resortSearch/', views.resortSearch, name='resortSearch'),
    path('reservations/', views.reservations, name='reservations'),
    path('checkCurrency/', views.checkCurrency, name='checkCurrency'),
    path('deleteReservations/<str:id>/',
         views.deleteReservations, name='deleteReservations'),
    path('delete_oneway_Reservations/<str:id>/',
         views.delete_oneway_Reservations, name='delete_oneway_Reservations'),
    path('delete_roundtrip_Reservations/<str:id>/',
         views.delete_roundtrip_Reservations, name='delete_roundtrip_Reservations'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('membership/', views.membership, name='membership'),
    path('userFeedback/', views.userFeedback, name='userFeedback'),
    path('payment/<int:price>/<str:name>/', views.payment, name='payment'),
    path('checkout_session/<int:price>/',
         views.checkout_session, name='checkout_session'),
    path('success2/', views.success2, name="success2"),
    path('error/', views.error, name="error"),
    path('offer/', views.offer, name="offer")
]
