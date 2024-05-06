# Generated by Django 5.0 on 2024-03-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0016_remove_flightclass_flight_id_delete_flight_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('airline_name', models.TextField()),
                ('airplane_name', models.TextField()),
                ('departure_city', models.TextField()),
                ('arrival_city', models.TextField()),
                ('departure_date', models.DateField()),
                ('arrival_date', models.DateField(blank=True, null=True)),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('flight_trip', models.TextField()),
                ('flight_class', models.TextField()),
                ('price', models.IntegerField()),
                ('airline_image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
    ]