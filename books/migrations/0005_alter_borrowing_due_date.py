# Generated by Django 5.1 on 2024-09-15 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_borrowing_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowing',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2024, 9, 29, 9, 30, 34, 128903, tzinfo=datetime.timezone.utc)),
        ),
    ]
