# Generated by Django 5.0 on 2024-03-23 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_offers_validfor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offers',
            name='validFor',
            field=models.CharField(max_length=200),
        ),
    ]
