# Generated by Django 4.1 on 2023-05-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("donut_app", "0010_order_paid"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="session_id",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
