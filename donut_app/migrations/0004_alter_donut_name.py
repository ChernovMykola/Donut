# Generated by Django 4.1 on 2023-04-28 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donut_app', '0003_orderitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donut',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]