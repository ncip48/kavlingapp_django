# Generated by Django 5.0.6 on 2024-09-05 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaksi', '0006_alter_cicilan_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='cicilan',
            name='pembayaran_ke',
            field=models.IntegerField(null=True),
        ),
    ]
