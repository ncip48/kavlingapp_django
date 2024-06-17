from django.db import models

# Create your models here.

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