from django.db import models
from django.contrib.auth.models import User


class singleFlightreservations(models.Model):
    reservation_id = models.CharField(max_length=20, unique=True)
    flight_id = models.CharField(
        max_length=20, blank=False, null=False, default=0)
    origin_code = models.CharField(max_length=200, null=False, blank=False)
    destination_code = models.CharField(
        max_length=200, null=False, blank=False)
    passenger_details = models.TextField(blank=False, null=False)
    airline = models.CharField(max_length=20, blank=False, null=False)
    departure = models.TextField(null=False, blank=False)
    arrival = models.TextField(null=False, blank=False)
    departure_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=True, blank=True)
    departure_time = models.TimeField(null=False, blank=False)
    arrival_time = models.TimeField(null=False, blank=False)
    flight_class = models.TextField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    flight_duration = models.CharField(
        max_length=20, blank=False, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.reservation_id:
            latest_reservation = singleFlightreservations.objects.order_by(
                '-reservation_id').first()
            if latest_reservation:
                last_id = int(latest_reservation.reservation_id.split('-')[1])
                new_id = f'R-{last_id + 1:03d}'
            else:
                new_id = 'R-001'

            self.reservation_id = new_id

        super().save(*args, **kwargs)


class doubleFlightreservations(models.Model):
    reservation_id = models.CharField(
        max_length=20, unique=True, null=False, blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    departure_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=False, blank=False)
    origin_code=models.CharField(max_length=20, null=False, blank=False)
    destination_code=models.CharField(max_length=20, null=False, blank=False)
    total_amount=models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.reservation_id:
            latest_reservation = doubleFlightreservations.objects.order_by(
                '-reservation_id').first()
            if latest_reservation:
                last_id = int(latest_reservation.reservation_id.split('-')[1])
                new_id = f'R-{last_id + 1:03d}'
            else:
                new_id = 'R-001'

            self.reservation_id = new_id

        super().save(*args, **kwargs)


class OutboundFlightDetails(models.Model):
    reservation_id = models.ForeignKey(
        doubleFlightreservations, on_delete=models.CASCADE)
    passenger_details = models.TextField(blank=True, null=True)
    origin_code = models.CharField(max_length=3, null=False, blank=False)
    departure_city = models.CharField(max_length=100, null=False, blank=False)
    destination_code = models.CharField(max_length=3, null=False, blank=False)
    arrival_city = models.CharField(max_length=100, null=False, blank=False)
    airline = models.CharField(max_length=100, null=False, blank=False)
    flight_id = models.CharField(max_length=10, null=False, blank=False)
    flight_class = models.CharField(max_length=50, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    flight_duration = models.CharField(
        max_length=20, blank=False, null=False, default=0)
    departure_time = models.TimeField(null=False, blank=False)
    arrival_time = models.TimeField(null=False, blank=False)


class InboundFlightDetails(models.Model):
    reservation_id = models.ForeignKey(
        doubleFlightreservations, on_delete=models.CASCADE)
    passenger_details = models.TextField(blank=True, null=True)
    origin_code = models.CharField(max_length=3, null=False, blank=False)
    departure_city = models.CharField(max_length=100, null=False, blank=False)
    destination_code = models.CharField(max_length=3, null=False, blank=False)
    arrival_city = models.CharField(max_length=100, null=False, blank=False)
    airline = models.CharField(max_length=100, null=False, blank=False)
    flight_id = models.CharField(max_length=10, null=False, blank=False)
    flight_class = models.CharField(max_length=50, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    flight_duration = models.CharField(
        max_length=20, blank=False, null=False, default=0)
    departure_time = models.TimeField(null=False, blank=False)
    arrival_time = models.TimeField(null=False, blank=False)
