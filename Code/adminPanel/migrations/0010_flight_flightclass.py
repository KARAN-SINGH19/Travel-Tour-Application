# Generated by Django 5.0 on 2024-03-01 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0009_remove_flightclass_flight_id_delete_flight_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('airline_name', models.TextField()),
                ('departure_city', models.TextField()),
                ('arrival_city', models.TextField()),
                ('departure_date', models.DateTimeField()),
                ('arrival_date', models.DateTimeField(blank=True, null=True)),
                ('is_round_trip', models.BooleanField(default=False)),
                ('flight_trip', models.TextField()),
                ('price', models.IntegerField()),
                ('airline_image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
        migrations.CreateModel(
            name='FlightClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_class', models.TextField(choices=[('Business', 'Business')])),
                ('price', models.IntegerField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminPanel.flight')),
            ],
        ),
    ]
