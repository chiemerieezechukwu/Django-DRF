# Generated by Django 4.0 on 2021-12-08 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_carratings_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='avg_rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='car',
            name='rates_number',
            field=models.IntegerField(default=0),
        ),
    ]
