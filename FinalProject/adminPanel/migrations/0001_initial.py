# Generated by Django 5.0 on 2024-02-13 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('airline_name', models.TextField()),
                ('departure_city', models.TextField()),
                ('arrival_city', models.TextField()),
                ('flight_class', models.TextField()),
                ('price', models.IntegerField()),
                ('departure_dateTime', models.DateTimeField()),
                ('arrival_dateTime', models.DateTimeField()),
                ('airline_image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('hotel_name', models.TextField()),
                ('hotel_location', models.TextField()),
                ('starting_price', models.IntegerField()),
                ('ratings', models.IntegerField()),
                ('hotel_image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
        migrations.CreateModel(
            name='Resort',
            fields=[
                ('resort_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('resort_name', models.TextField()),
                ('resort_location', models.TextField()),
                ('starting_price', models.IntegerField()),
                ('ratings', models.IntegerField()),
                ('resort_image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
    ]
