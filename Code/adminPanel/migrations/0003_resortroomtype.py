# Generated by Django 5.0 on 2024-02-15 08:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0002_hotelroomtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='resortRoomtype',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('room_type', models.TextField()),
                ('room_price', models.IntegerField()),
                ('resort_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminPanel.resort')),
            ],
        ),
    ]
