# Generated by Django 5.0 on 2024-03-01 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0010_flight_flightclass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightclass',
            name='flight_id',
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
        migrations.DeleteModel(
            name='FlightClass',
        ),
    ]
