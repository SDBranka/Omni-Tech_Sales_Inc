# Generated by Django 2.2 on 2021-07-09 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgfield_app', '0016_auto_20210708_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='placed_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 9, 3, 50, 24, 420778)),
        ),
    ]
