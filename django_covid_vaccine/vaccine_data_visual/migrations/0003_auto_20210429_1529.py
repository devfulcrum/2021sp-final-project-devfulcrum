# Generated by Django 3.2 on 2021-04-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine_data_visual', '0002_auto_20210429_1316'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='coviddata',
            table='covid_data',
        ),
        migrations.AlterModelTable(
            name='vaccinedata',
            table='vaccine_data',
        ),
    ]
