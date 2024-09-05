from django.db import models
from customer.models import Customer
from kavling.models import Kavling
from marketing.models import Marketing
import uuid
from terbilang import Terbilang

# Create your models here.
class Transaksi(models.Model):
    class TransaksiTipe(models.IntegerChoices):
        BOOKING = 0, "Booking"
        CASH = 1, "Cash"
        KREDIT = 2, "Kredit"
        
    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    tanggal_transaksi = models.DateField(null=True)
    kavling = models.ForeignKey(Kavling, on_delete=models.CASCADE)
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
        
    @property
    def terbilang(self):
        terbilang =  Terbilang()
        if self.tipe_transaksi == Transaksi.TransaksiTipe.BOOKING:
            terbilang.parse(self.pembelian_booking)
        elif self.tipe_transaksi == Transaksi.TransaksiTipe.CASH:
            terbilang.parse(self.pembayaran_cash)
        else:
            terbilang.parse(self.dp)
        return terbilang.getresult().title()
    
    @property
    def kavling_instance(self):
        return self.kavling