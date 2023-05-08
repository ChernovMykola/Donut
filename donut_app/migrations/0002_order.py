# Generated by Django 4.1 on 2023-04-26 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('donut_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.CharField(max_length=100)),
                ('customer_adress', models.CharField(max_length=100)),
                (
                    'donut_name',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='donut_app.donut',
                    ),
                ),
            ],
        ),
    ]
