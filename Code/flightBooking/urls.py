from django.contrib import admin
from django.urls import path, include
from flightBooking import views
app_name = 'flightBooking'

urlpatterns = [
    path('selectDoubleflight/', views.selectDoubleflight,
         name="selectDoubleflight"),
    path('selectSingleflight/', views.selectSingleflight,
         name="selectSingleflight"),
    path('confirmSingleflight/<str:origincode>/<str:destinationcode>/<str:airline>/<str:id>/<str:duration>/<int:passengers>/<int:price>/<int:finalFare>/<str:deptDate>/<str:returnDate>/<str:deptTime>/<str:arrTime>/<str:deptCity>/<str:arrCity>/<str:airlineName>/<str:flightId>/<str:flightClass>/<path:image>/',
         views.confirmSingleflight, name='confirmSingleflight'),
    path('confirmDoubleflight/<path:image>/<str:departure_date>/<str:return_date>/<str:flightClass>/<int:passengers>/', views.confirmDoubleflight,
         name='confirmDoubleflight'),
    path('generateFlightreceipt1/', views.generateFlightreceipt1,
         name="generateFlightreceipt1"),
    path('generateFlightreceipt2/<int:passengers>/<int:Totalamt>/<int:OutboundFinalfare>/<int:InboundFinalfare>/', views.generateFlightreceipt2,
         name="generateFlightreceipt2"),
    path('checkout_session1/', views.checkout_session1, name='checkout_session1'),
    path('checkout_session2/<int:Totalamt>/',
         views.checkout_session2, name='checkout_session2'),
    path('ticket/', views.ticket, name='ticket'),
    path('ticket2/', views.ticket2, name='ticket2'),
    path('sendEmail/<str:id>/', views.sendEmail, name='sendEmail'),
    path('sendEmail2/<str:id>/', views.sendEmail2, name='sendEmail2'),
    path('notFound/',views.notFound,name='notFound')
]
