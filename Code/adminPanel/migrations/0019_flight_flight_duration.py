# Generated by Django 5.0 on 2024-03-03 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0018_rename_arrival_date_flight_return_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='flight_duration',
            field=models.TextField(default=0),
        ),
    ]