# Generated by Django 5.0.6 on 2024-06-12 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstore', '0007_site_placement_template'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tanggal_transaksi', models.DateField(null=True)),
                ('tipe_transaksi', models.CharField(max_length=50)),
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
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstore.customer')),
                ('id_kavling', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstore.kavling')),
                ('marketing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]