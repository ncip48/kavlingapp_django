from django.forms import ModelForm, DateInput
from django.utils.translation import gettext_lazy as _
from transaksi.models import *

class DateInput(DateInput):
    input_type = 'date'
class TransaksiForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].required = True
    #     self.fields['first_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = False
        
    class Meta:
        # merelasikan form dengan model
        model = Transaksi
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('tanggal_transaksi', 'tipe_transaksi', 'fee_marketing', 'fee_notaris')
        widgets = {
            'tanggal_transaksi': DateInput(),
        }
        # mengatur teks label untuk setiap field
        labels = {
            'tanggal_transaksi': _('Tanggal Transaksi'),
            'tipe_transaksi': _('Tipe Transaksi'),
            'fee_marketing': _('Fee Marketing'),
            'fee_notaris': _('Fee Notaris'),
        }
        
class TransaksiFormCash(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].required = True
    #     self.fields['first_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = False
        
    class Meta:
        # merelasikan form dengan model
        model = Transaksi
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('pembayaran_cash', 'keterangan',)
        # mengatur teks label untuk setiap field
        labels = {
            'pembayaran_cash': _('Pembayaran Cash'),
            'keterangan': _('Keterangan'),
        }
        
class TransaksiFormKredit(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].required = True
    #     self.fields['first_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = False
        
    class Meta:
        # merelasikan form dengan model
        model = Transaksi
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('dp', 'tenor', 'cicilan_per_bulan', 'tanggal_tempo', 'keterangan',)
        # mengatur teks label untuk setiap field
        labels = {
            'dp': _('DP'),
            'tenor': _('Tenor'),
            'cicilan_per_bulan': _('Cicilan Per Bulan'),
            'tanggal_tempo': _('Tanggal Tempo'),
            'keterangan': _('Keterangan'),
        }