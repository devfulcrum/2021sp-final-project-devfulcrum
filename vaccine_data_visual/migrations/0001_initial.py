# Generated by Django 3.2 on 2021-04-17 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_region', models.CharField(max_length=75)),
                ('date', models.DateField()),
                ('doses_administered', models.IntegerField()),
                ('people_partially_vaccinated', models.IntegerField()),
                ('people_fully_vaccinated', models.IntegerField()),
                ('report_date_string', models.CharField(max_length=15)),
                ('uid', models.CharField(max_length=20)),
            ],
        ),
    ]
