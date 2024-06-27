# Generated by Django 5.0.6 on 2024-06-17 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('logo', models.FileField(null=True, upload_to='')),
                ('nama_website', models.CharField(max_length=50)),
                ('nama_perusahaan', models.CharField(max_length=50)),
                ('alamat', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('template_kavling', models.TextField()),
                ('no_telp', models.CharField(max_length=15, null=True)),
                ('no_hp', models.CharField(max_length=15)),
                ('placement_template', models.TextField()),
                ('ttd', models.FileField(null=True, upload_to='')),
            ],
            options={
                'db_table': 'site',
            },
        ),
    ]