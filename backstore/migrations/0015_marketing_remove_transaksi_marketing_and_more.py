# Generated by Django 5.0.6 on 2024-06-17 01:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstore', '0014_alter_kavling_harga_jual_cash_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('nik', models.CharField(max_length=20, unique=True)),
                ('alamat', models.TextField()),
                ('jk', models.IntegerField(choices=[(0, 'Laki-Laki'), (1, 'Perempuan')], default=0)),
                ('no_hp', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='transaksi',
            name='marketing',
        ),
        migrations.AlterField(
            model_name='customer',
            name='nik',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='transaksi',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backstore.marketing'),
        ),
    ]