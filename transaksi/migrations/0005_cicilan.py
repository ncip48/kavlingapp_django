# Generated by Django 5.0.6 on 2024-09-05 06:05

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaksi', '0004_rename_id_kavling_transaksi_kavling'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cicilan',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nominal', models.IntegerField()),
                ('transaksi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaksi.transaksi')),
            ],
        ),
    ]