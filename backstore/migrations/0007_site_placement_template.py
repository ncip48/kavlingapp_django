# Generated by Django 5.0.6 on 2024-06-12 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstore', '0006_alter_customer_kk_alter_customer_ktp'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='placement_template',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]