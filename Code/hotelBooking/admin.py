from django.contrib import admin
from hotelBooking.models import *
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'reservation_type','reservation_room','reservation_location', 'reservation_amount', 'reservation_dateTime', 'username')
admin.site.register(Reservation, ReservationAdmin)