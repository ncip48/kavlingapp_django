# Generated by Django 5.0.6 on 2024-06-09 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backstore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kavling',
            name='is_cash',
        ),
        migrations.AlterModelTable(
            name='kavling',
            table='kavling',
        ),
    ]