from django.db import models
from customer.models import Customer
from kavling.models import Kavling
from marketing.models import Marketing

# Create your models here.
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