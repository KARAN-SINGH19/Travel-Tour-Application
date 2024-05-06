from django.urls import path
from adminPanel import views
app_name='adminPanel'

urlpatterns = [
    path('', views.adminHome, name='admin'),
    path('addHotel/', views.addHotels, name='addHotel'),
    path('addResort/', views.addResorts, name='addResort'),
    path('addFlight/', views.addFlights, name='addFlight'),
    path('viewHotel/', views.viewHotel, name='viewHotel'),
    path('viewResort/', views.viewResort, name='viewResort'),
    path('viewFlight/', views.viewFlight, name='viewFlight'),
    path('editHotel/', views.editHotel, name='editHotel'),
    path('editResort/', views.editResort, name='editResort'),
    path('editFlight/', views.editFlight, name='editFlight'),
    path('deleteHotel/<str:id>', views.deleteHotel, name='deleteHotel'),
    path('deleteResort/<str:id>', views.deleteResort, name='deleteResort'),
    path('deleteFlight/<str:id>', views.deleteFlight, name='deleteFlight'),
    path('updateHotel/<str:id>', views.updateHotel, name='updateHotel'),
    path('updateHotelDetails/<str:id>', views.updateHotelDetails, name='updateHotelDetails'),
    path('updateResort/<str:id>', views.updateResort, name='updateResort'),
    path('updateResortDetails/<str:id>', views.updateResortDetails, name='updateResortDetails'),
    path('updateFlight/<str:id>', views.updateFlight, name='updateFlight'),
    path('updateFlightDetails/<str:id>', views.updateFlightDetails, name='updateFlightDetails'),
    path('logout_user/', views.logout_user, name='logout_user'),
]
