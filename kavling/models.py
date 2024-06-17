from django.db import models

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
        from transaksi.models import Transaksi
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