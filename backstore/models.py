from django.db import models
from enum import Enum

# Create your models here.
class Kavling(models.Model):
    
    class KavlingStatus(models.IntegerChoices):
        TERSEDIA = 0, "Tersedia"
        BOOKING = 1, "Booking"
        TERJUAL = 2, "Terjual"
    
    id = models.AutoField(primary_key=True)
    kode_kavling = models.CharField(max_length=10)
    luas_tanah = models.IntegerField()
    harga_per_meter = models.IntegerField()
    harga_jual_cash = models.IntegerField()
    map_code = models.TextField()
    status = models.IntegerField(
        choices=KavlingStatus.choices, 
        default=KavlingStatus.TERSEDIA
    )
    
    class Meta:
        # define table name
        db_table = 'kavling'
        
class Site(models.Model):
    
    id = models.AutoField(primary_key=True)
    logo = models.CharField(max_length=50)
    nama_website = models.CharField(max_length=50)
    nama_perusahaan = models.CharField(max_length=50)
    template_kavling = models.TextField()
    no_hp = models.CharField(max_length=15)
    
    class Meta:
        # define table name
        db_table = 'site'
