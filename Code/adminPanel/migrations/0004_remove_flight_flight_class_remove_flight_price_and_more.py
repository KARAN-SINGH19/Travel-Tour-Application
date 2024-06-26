# Generated by Django 5.0 on 2024-02-27 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0003_resortroomtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='flight_class',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='price',
        ),
        migrations.CreateModel(
            name='FlightClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_class', models.TextField(choices=[('Economy', 'Economy'), ('Business', 'Business')])),
                ('price', models.IntegerField()),
                ('flight_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminPanel.flight')),
            ],
        ),
    ]
