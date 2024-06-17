# Generated by Django 5.0.6 on 2024-06-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=50)),
                ('nik', models.CharField(max_length=20, unique=True)),
                ('tempat_lahir', models.CharField(max_length=20, null=True)),
                ('tanggal_lahir', models.DateField(null=True)),
                ('alamat', models.TextField()),
                ('jk', models.IntegerField(choices=[(0, 'Laki-Laki'), (1, 'Perempuan')], default=0)),
                ('no_hp', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('pekerjaan', models.CharField(max_length=100, null=True)),
                ('ktp', models.FileField(null=True, upload_to='')),
                ('kk', models.FileField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
    ]
