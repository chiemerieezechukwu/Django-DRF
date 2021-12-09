# Generated by Django 4.0 on 2021-12-08 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_car_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='avg_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
