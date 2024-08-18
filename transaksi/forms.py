from django.forms import ModelForm, DateInput, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from transaksi.models import *

class CustomerModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama} | {obj.no_hp}"
    
class MarketingModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama} | {obj.no_hp}"
class DateInput(DateInput):
    input_type = 'date'
class TransaksiForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].required = True
    #     self.fields['first_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = False

    customer = CustomerModelChoiceField(queryset=Customer.objects.all(),empty_label="Pilih Customer",to_field_name="id")        
    marketing = MarketingModelChoiceField(queryset=Marketing.objects.all(),empty_label="Pilih Marketing",to_field_name="id")        
    class Meta:
        # merelasikan form dengan model
        model = Transaksi
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('tanggal_transaksi', 'customer', 'marketing', 'tipe_transaksi', 'fee_marketing', 'fee_notaris')
        widgets = {
            'tanggal_transaksi': DateInput(),
        }
        # mengatur teks label untuk setiap field
        labels = {
            'tanggal_transaksi': _('Tanggal Transaksi'),
            'customer': _('Customer'),
            'tipe_transaksi': _('Tipe Transaksi'),
            'fee_marketing': _('Fee Marketing'),
            'fee_notaris': _('Fee Notaris'),
        }
        
class TransaksiFormCash(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keterangan'].required = False
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keterangan'].required = False
    #     self.fields['first_name'].required = True
    #     self.fields['email'].required = True
    #     self.fields['password'].required = False
        
    class Meta:
        # merelasikan form dengan model
        model = Transaksi
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('dp', 'tenor', 'cicilan_per_bulan', 'tanggal_tempo', 'keterangan',)
        widgets = {
            'tanggal_tempo': DateInput(),
        }
        # mengatur teks label untuk setiap field
        labels = {
            'dp': _('DP'),
            'tenor': _('Tenor'),
            'cicilan_per_bulan': _('Cicilan Per Bulan'),
            'tanggal_tempo': _('Tanggal Tempo'),
            'keterangan': _('Keterangan'),
        }
        
class TransaksiFormBooking(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keterangan'].required = False
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
        fields = ('pembelian_booking', 'tanggal_batas_booking', 'keterangan',)
        widgets = {
            'tanggal_batas_booking': DateInput(),
        }
        # mengatur teks label untuk setiap field
        labels = {
            'pembelian_booking': _('Uang Muka'),
            'tanggal_batas_booking': _('Tanggal Batas Booking'),
            'keterangan': _('Keterangan'),
        }