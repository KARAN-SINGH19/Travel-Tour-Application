from django.contrib import admin
from flightBooking.models import *


class singleFlightreservationsAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'flight_id', 'origin_code', 'destination_code', 'passenger_details', 'airline',
                    'departure', 'arrival', 'departure_date', 'return_date', 'departure_time', 'arrival_time', 'flight_class', 'price', 'flight_duration', 'flight_class', 'username')


class doubleFlightreservationsAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'username',
                    'departure_date', 'return_date','origin_code','destination_code','total_amount')


class OutboundFlightDetailsAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'passenger_details', 'origin_code', 'destination_code', 'departure_city', 'arrival_city',
                    'airline', 'flight_id', 'flight_class', 'price', 'flight_duration', 'departure_time', 'arrival_time')


class InboundFlightDetailsAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'passenger_details', 'origin_code', 'destination_code', 'departure_city', 'arrival_city',
                    'airline', 'flight_id', 'flight_class', 'price', 'flight_duration', 'departure_time', 'arrival_time')


admin.site.register(singleFlightreservations, singleFlightreservationsAdmin)
admin.site.register(doubleFlightreservations, doubleFlightreservationsAdmin)
admin.site.register(OutboundFlightDetails, OutboundFlightDetailsAdmin)
admin.site.register(InboundFlightDetails, InboundFlightDetailsAdmin)
