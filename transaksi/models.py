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
    def nominal_awal(self):
        if self.tipe_transaksi == Transaksi.TransaksiTipe.BOOKING:
            return self.pembelian_booking
        elif self.tipe_transaksi == Transaksi.TransaksiTipe.CASH:
            return self.pembayaran_cash
        else:
            return self.dp
    
    
    @property
    def untuk_pembayaran(self):
        if self.tipe_transaksi == Transaksi.TransaksiTipe.BOOKING:
            return f'Booking Kavling {self.kavling.kode_kavling}'
        elif self.tipe_transaksi == Transaksi.TransaksiTipe.CASH:
            return f'Pembelian Kavling {self.kavling.kode_kavling}'
        else:
            return f'DP Kavling {self.kavling.kode_kavling}'
        
    
    @property
    def kavling_instance(self):
        return self.kavling
    
    @property
    def customer_instance(self):
        return self.customer
    
    @property
    def cicilan(self):
        return Cicilan.objects.filter(transaksi_id=self.id)
    
    @property
    def sisa_cicilan(self):
        numbers = [cicilan.nominal for cicilan in self.cicilan]
    
        # Convert each number from string to integer
        numbers_int = [int(x) for x in numbers]
        
        # Calculate the sum of all integers
        total_cicilan = sum(numbers_int)
            
        return self.kavling.harga_jual_cash - (total_cicilan)
    
    @property
    def tempo(self):
        return self.tanggal_tempo.strftime("%d")
    
    @property
    def format_tanggal_tempo(self):
        return f'Tanggal {self.tanggal_tempo.strftime("%d")}'
    
    @property
    def cicilan_terakhir(self):
        latest_cicilan = Cicilan.objects.filter(transaksi=self).order_by('-tanggal_pembayaran').first()
        return latest_cicilan
    
    @property
    def pembayaran_terakhir_ke(self):
        last = self.cicilan_terakhir
        if last is None:
            return 1
        else:
            return self.cicilan_terakhir.pembayaran_ke + 1
    
class Cicilan(models.Model):
    id = models.AutoField(primary_key=True)
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    transaksi = models.ForeignKey(Transaksi, on_delete=models.CASCADE)
    pembayaran_ke = models.IntegerField(null=True)
    nominal = models.IntegerField()
    tanggal_pembayaran = models.DateField(null=True)
    
    class Meta:
        # define table name
        db_table = 'cicilan'
        
    @property
    def terbilang(self):
        terbilang =  Terbilang()
        terbilang.parse(self.nominal)
        return terbilang.getresult().title()
    
    @property
    def transaksi_instance(self):
        return self.transaksi
    
    @property
    def cicilan_text(self):
        return f'Pembayaran cicilan kavling {self.transaksi.kavling.kode_kavling} ke {self.pembayaran_ke}'
    
    @property
    def format_tanggal(self):
        return self.tanggal_pembayaran.strftime("%d %b %Y")
    
    @property
    def sisa(self):
        # Get the total nominal value for all previous payments
        total_nominal_before = self._calculate_total_nominal_before()
        
        # Calculate sisa based on the current pembayaran_ke
        if self.pembayaran_ke == 1:
            sisa = self.transaksi.kavling.harga_jual_cash - self.transaksi.dp - self.nominal
        else:
            sisa = self.transaksi.kavling.harga_jual_cash - self.transaksi.dp - total_nominal_before - self.nominal
        
        return max(sisa,0)

    def _calculate_total_nominal_before(self):
        """
        Calculate the total nominal value of all payments before the current pembayaran_ke.
        """
        total_nominal = Cicilan.objects.filter(
            transaksi=self.transaksi,
            pembayaran_ke__lt=self.pembayaran_ke
        ).aggregate(total_nominal=models.Sum('nominal'))['total_nominal'] or 0
        
        return total_nominal