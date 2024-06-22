from django.db import models
import uuid

# Create your models here.
class Kavling(models.Model):
    
    class KavlingStatus(models.IntegerChoices):
        TERSEDIA = 0, "Tersedia"
        BOOKING = 1, "Booking"
        TERJUAL = 2, "Terjual"
    
    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
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
    def clean_g(self):
        g = self.map_code_g
        return g.replace('<g', '').replace('>', '')
        
    @property
    def transaksi(self):
        from transaksi.models import Transaksi
        return Transaksi.objects.get(kavling_id=self.id)
        
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
        
    @property
    def get_status_real(self):
        if self.status == 0:
            return "Tersedia"
        elif self.status == 1:
            if self.transaksi.tipe_transaksi ==0:
                return "Booking"
        elif self.status == 2:
            if self.transaksi.tipe_transaksi == 1:
                return "Terjual Cash"
            elif self.transaksi.tipe_transaksi == 2:
                return "Terjual Kredit"