from django.db import models
from enum import Enum
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

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
    map_code_g = models.TextField()
    map_code_path = models.TextField()
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

class User(AbstractUser):
    
    class UserRole(models.IntegerChoices):
        ADMIN = 0, "Admin"
        MARKETING = 1, "Marketing"
        CUSTOMER = 2, "Customer"
    
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role = models.IntegerField(
        choices=UserRole.choices, 
        default=UserRole.ADMIN
    )
    phone = models.CharField(max_length=15)
    
    @property
    def name(self):
        # due date is calcualted 10 days from start_date
        return self.first_name + self.last_name
    
class Customer(models.Model):
    class JenisKelamin(models.IntegerChoices):
        LAKILAKI = 0, "Laki-Laki"
        PEREMPUAN = 1, "Perempuan"
        
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    nik = models.CharField(max_length=20)
    tempat_lahir = models.CharField(max_length=20, null=True)
    tanggal_lahir = models.DateField(null=True)
    alamat = models.TextField()
    jk = models.IntegerField(
        choices=JenisKelamin.choices, 
        default=JenisKelamin.LAKILAKI
    )
    no_hp = models.CharField(max_length=15)
    email = models.EmailField()
    pekerjaan = models.CharField(null=True, max_length=100)
    ktp = models.FileField(null=True, max_length=100)
    kk = models.FileField(null=True, max_length=100)
    class Meta:
        # define table name
        db_table = 'customer'