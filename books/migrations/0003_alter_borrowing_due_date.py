# Generated by Django 5.1 on 2024-09-14 21:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_remove_borrowing_borrowed_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowing',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 9, 28, 21, 13, 13, 584664, tzinfo=datetime.timezone.utc)),
        ),
    ]
