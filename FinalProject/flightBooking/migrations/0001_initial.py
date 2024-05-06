# Generated by Django 5.0 on 2024-03-09 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='doubleFlightreservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.CharField(max_length=20, unique=True)),
                ('departure_date', models.DateField()),
                ('return_date', models.DateField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InboundFlightDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_details', models.TextField(blank=True, null=True)),
                ('origin_code', models.CharField(max_length=3)),
                ('departure_city', models.CharField(max_length=100)),
                ('destination_code', models.CharField(max_length=3)),
                ('arrival_city', models.CharField(max_length=100)),
                ('airline', models.CharField(max_length=100)),
                ('flight_id', models.CharField(max_length=10)),
                ('flight_class', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('flight_duration', models.CharField(default=0, max_length=20)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('reservation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightBooking.doubleflightreservations')),
            ],
        ),
        migrations.CreateModel(
            name='OutboundFlightDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_details', models.TextField(blank=True, null=True)),
                ('origin_code', models.CharField(max_length=3)),
                ('departure_city', models.CharField(max_length=100)),
                ('destination_code', models.CharField(max_length=3)),
                ('arrival_city', models.CharField(max_length=100)),
                ('airline', models.CharField(max_length=100)),
                ('flight_id', models.CharField(max_length=10)),
                ('flight_class', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('flight_duration', models.CharField(default=0, max_length=20)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('reservation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flightBooking.doubleflightreservations')),
            ],
        ),
        migrations.CreateModel(
            name='singleFlightreservations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.CharField(max_length=20, unique=True)),
                ('flight_id', models.CharField(default=0, max_length=20)),
                ('origin_code', models.CharField(max_length=200)),
                ('destination_code', models.CharField(max_length=200)),
                ('passenger_details', models.TextField()),
                ('airline', models.CharField(max_length=20)),
                ('departure', models.TextField()),
                ('arrival', models.TextField()),
                ('departure_date', models.DateField()),
                ('return_date', models.DateField(blank=True, null=True)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('flight_class', models.TextField()),
                ('price', models.IntegerField()),
                ('flight_duration', models.CharField(max_length=20)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]