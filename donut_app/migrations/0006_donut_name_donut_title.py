# Generated by Django 4.1 on 2023-04-28 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donut_app', '0005_remove_donut_name_remove_donut_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='donut',
            name='name',
            field=models.CharField(default='New Donut', max_length=200),
        ),
        migrations.AddField(
            model_name='donut',
            name='title',
            field=models.CharField(default='New Donut', max_length=200),
        ),
    ]