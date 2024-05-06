from django.db import models


class Hotel(models.Model):
    hotel_id = models.CharField(
        max_length=200, primary_key=True, null=False, blank=False)
    hotel_name = models.TextField(null=False, blank=False)
    hotel_location = models.TextField(null=False, blank=False)
    starting_price = models.IntegerField(null=False, blank=False)
    ratings = models.IntegerField(null=False, blank=False)
    hotel_image = models.ImageField(
        upload_to='uploads/images',  null=False, blank=False)


class Resort(models.Model):
    resort_id = models.CharField(
        max_length=200, primary_key=True, null=False, blank=False)
    resort_name = models.TextField(null=False, blank=False)
    resort_location = models.TextField(null=False, blank=False)
    starting_price = models.IntegerField(null=False, blank=False)
    ratings = models.IntegerField(null=False, blank=False)
    resort_image = models.ImageField(
        upload_to='uploads/images',  null=False, blank=False)


class Flight(models.Model):
    flight_id = models.CharField(
        max_length=200, primary_key=True, null=False, blank=False)
    origin_code = models.CharField(max_length=200, null=False, blank=False)
    destination_code = models.CharField(
        max_length=200, null=False, blank=False)
    airline_name = models.TextField(null=False, blank=False)
    airplane_name = models.TextField(null=False, blank=False)
    departure_city = models.TextField(null=False, blank=False)
    arrival_city = models.TextField(null=False, blank=False)
    departure_date = models.DateField(null=False, blank=False)
    return_date = models.DateField(null=True, blank=True)
    departure_time = models.TimeField(null=False, blank=False)
    arrival_time = models.TimeField(null=False, blank=False)
    flight_trip = models.TextField(null=False, blank=False)
    flight_class = models.TextField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    flight_duration = models.TextField(null=False, blank=False, default=0)
    airline_image = models.ImageField(
        upload_to='uploads/images',  null=False, blank=False)


class hotelRoomtype(models.Model):
    room_id = models.IntegerField(primary_key=True, blank=False, null=False)
    room_type = models.TextField(blank=False, null=False)
    room_price = models.IntegerField(blank=False, null=False)
    room_capacity = models.IntegerField(blank=False, null=False, default=0)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)


class resortRoomtype(models.Model):
    room_id = models.IntegerField(primary_key=True, blank=False, null=False)
    room_type = models.TextField(blank=False, null=False)
    room_price = models.IntegerField(blank=False, null=False)
    room_capacity = models.IntegerField(blank=False, null=False, default=0)
    resort_id = models.ForeignKey(Resort, on_delete=models.CASCADE)
