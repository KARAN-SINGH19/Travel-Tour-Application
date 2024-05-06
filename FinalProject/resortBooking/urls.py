from django.contrib import admin
from django.urls import path, include
from resortBooking import views
app_name = 'resortBooking'

urlpatterns = [
    path('bookResort/<str:id>/<str:name>/<str:location>/<path:image>/',
         views.bookResort, name='bookResort'),
    path('confirmBooking/<str:id>/<str:name>/<str:location>/<str:roomType>/<int:roomPrice>/',
         views.confirmBooking, name='confirmBooking'),
    path('generateReceipt/', views.generateReceipt, name='generateReceipt'),
    path('checkout_session/<str:id>/',
         views.checkout_session, name='checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
