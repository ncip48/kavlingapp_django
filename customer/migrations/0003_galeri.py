# Generated by Django 5.0.6 on 2024-09-05 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_customer_foto_orang'),
    ]

    operations = [
        migrations.CreateModel(
            name='Galeri',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keterangan', models.TextField()),
                ('foto', models.FileField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'galeri',
            },
        ),
    ]
