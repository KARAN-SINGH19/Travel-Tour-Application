from django.contrib import admin
from adminPanel.models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_id', 'hotel_name', 'hotel_location',
                    'starting_price', 'ratings', 'hotel_image')


class ResortAdmin(admin.ModelAdmin):
    list_display = ('resort_id', 'resort_name', 'resort_location',
                    'starting_price', 'ratings', 'resort_image')


class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id', 'airline_name', 'origin_code', 'destination_code', 'airplane_name', 'departure_city',
                    'arrival_city', 'departure_date', 'return_date', 'departure_time', 'arrival_time', 'flight_trip', 'flight_class', 'price', 'flight_duration', 'airline_image')


class hotelRoomtypeAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_type', 'room_capacity',
                    'room_price', 'hotel_id')


class resortRoomtypeAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_type', 'room_capacity',
                    'room_price', 'resort_id')


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Resort, ResortAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(hotelRoomtype, hotelRoomtypeAdmin)
admin.site.register(resortRoomtype, resortRoomtypeAdmin)
