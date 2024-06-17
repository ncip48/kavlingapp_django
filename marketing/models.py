from django.db import models
# from transaksi.models import Transaksi

# Create your models here.
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
        from transaksi.models import Transaksi  # Import inside the method to avoid circular import
        return Transaksi.objects.filter(marketing_id=self.id, is_lunas=0).count()
    
    @property
    def penjualan_close(self):
        from transaksi.models import Transaksi  # Import inside the method to avoid circular import
        return Transaksi.objects.filter(marketing_id=self.id, is_lunas=1).count()
