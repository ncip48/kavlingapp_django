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
    harga_per_meter = models.IntegerField(null=True)
    harga_jual_cash = models.IntegerField(null=True)
    map_code_g = models.TextField(null=True)
    map_code_path = models.TextField(null=True)
    text_code_svg = models.TextField(null=True)
    status = models.IntegerField(
        choices=KavlingStatus.choices, 
        default=KavlingStatus.TERSEDIA
    )
    
    class Meta:
        # define table name
        db_table = 'kavling'
        
    @property
    def transaksi(self):
        return Transaksi.objects.get(id_kavling=self.id)
        
    @property
    def get_color(self):
        if self.status == 0:
            return "white"
        elif self.status == 1:
            if self.transaksi.tipe_transaksi ==0:
                return "blue"
        elif self.status == 2:
            if self.transaksi.tipe_transaksi == 1:
                return "green"
            elif self.transaksi.tipe_transaksi == 2:
                return "red"
        
    @property
    def get_font_color(self):
        if self.status == 0:
            return "black"
        elif self.status == 1:
            return "white"
        elif self.status == 2:
            return "white"
        
        
class Site(models.Model):
    id = models.AutoField(primary_key=True)
    logo = models.CharField(max_length=50)
    nama_website = models.CharField(max_length=50)
    nama_perusahaan = models.CharField(max_length=50)
    template_kavling = models.TextField()
    no_hp = models.CharField(max_length=15)
    placement_template = models.TextField()
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
    
class Marketing(models.Model):
    class JenisKelamin(models.IntegerChoices):
        LAKILAKI = 0, "Laki-Laki"
        PEREMPUAN = 1, "Perempuan"
        
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    nik = models.CharField(max_length=20, unique=True)
    alamat = models.TextField()
    jk = models.IntegerField(
        choices=JenisKelamin.choices, 
        default=JenisKelamin.LAKILAKI
    )
    no_hp = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    class Meta:
        # define table name
        db_table = 'marketing'
        
    @property
    def penjualan_progress(self):
        return Transaksi.objects.filter(marketing_id=self.id, is_lunas=0).count()
    
    def penjualan_close(self):
        return Transaksi.objects.filter(marketing_id=self.id, is_lunas=1).count()
    
class Customer(models.Model):
    class JenisKelamin(models.IntegerChoices):
        LAKILAKI = 0, "Laki-Laki"
        PEREMPUAN = 1, "Perempuan"
        
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    nik = models.CharField(max_length=20, unique=True)
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
        
class Transaksi(models.Model):
    class TransaksiTipe(models.IntegerChoices):
        BOOKING = 0, "Booking"
        CASH = 1, "Cash"
        KREDIT = 2, "Kredit"
        
    id = models.AutoField(primary_key=True)
    tanggal_transaksi = models.DateField(null=True)
    id_kavling = models.ForeignKey(Kavling, on_delete=models.CASCADE)
    tipe_transaksi = models.IntegerField(
        choices=TransaksiTipe.choices, 
        default=TransaksiTipe.BOOKING
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    marketing = models.ForeignKey(Marketing, on_delete=models.CASCADE)
    fee_marketing = models.IntegerField()
    fee_notaris = models.IntegerField()
    dp = models.IntegerField(null=True)
    tenor = models.IntegerField(null=True)
    cicilan_per_bulan = models.IntegerField(null=True)
    tanggal_tempo = models.DateField(null=True)
    pembayaran_cash = models.IntegerField(null=True)
    pembelian_booking = models.IntegerField(null=True)
    tanggal_batas_booking = models.DateField(null=True)
    keterangan = models.TextField(null=True)
    is_lunas = models.IntegerField(null=True, default=0)
    class Meta:
        # define table name
        db_table = 'transaksi'
