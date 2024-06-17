# Generated by Django 5.0.6 on 2024-06-17 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('kavling', '0001_initial'),
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_transaksi', models.DateField(null=True)),
                ('tipe_transaksi', models.IntegerField(choices=[(0, 'Booking'), (1, 'Cash'), (2, 'Kredit')], default=0)),
                ('fee_marketing', models.IntegerField()),
                ('fee_notaris', models.IntegerField()),
                ('dp', models.IntegerField(null=True)),
                ('tenor', models.IntegerField(null=True)),
                ('cicilan_per_bulan', models.IntegerField(null=True)),
                ('tanggal_tempo', models.DateField(null=True)),
                ('pembayaran_cash', models.IntegerField(null=True)),
                ('pembelian_booking', models.IntegerField(null=True)),
                ('tanggal_batas_booking', models.DateField(null=True)),
                ('keterangan', models.TextField(null=True)),
                ('is_lunas', models.IntegerField(default=0, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('id_kavling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kavling.kavling')),
                ('marketing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketing.marketing')),
            ],
            options={
                'db_table': 'transaksi',
            },
        ),
    ]
