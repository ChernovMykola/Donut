# Generated by Django 4.1 on 2023-04-23 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('picture', models.ImageField(upload_to='donut_pictures')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('stars', models.IntegerField()),
                ('labels', models.CharField(choices=[('GF', 'Gluten-Free'), ('VE', 'Vegan')], max_length=2)),
                ('ingredients', models.TextField()),
                ('allergens', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('count', models.IntegerField()),
            ],
        ),
    ]