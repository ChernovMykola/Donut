# Generated by Django 4.1 on 2023-05-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('donut_app', '0009_alter_donut_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
