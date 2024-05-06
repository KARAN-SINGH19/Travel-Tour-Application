from django.contrib import admin
from django.urls import path, include
from hotelBooking import views
app_name = 'hotelBooking'

urlpatterns = [
    path('bookHotel/<str:id>/<str:name>/<str:location>/<path:image>/',
         views.bookHotel, name='bookHotel'),
    path('confirmBooking/<str:id>/<str:name>/<str:location>/<str:roomType>/<int:roomPrice>/',
         views.confirmBooking, name='confirmBooking'),
    path('generateReceipt/', views.generateReceipt, name='generateReceipt'),
    path('checkout_session/<str:id>/',
         views.checkout_session, name='checkout_session'),
    path('hotelPass/', views.hotelPass, name='hotelPass'),
    path('sendEmail/<str:id>/<str:type>/', views.sendEmail, name='sendEmail'),
    path('invalidCode/', views.invalidCode, name="invalidCode")
]
