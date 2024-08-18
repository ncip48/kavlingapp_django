from django.forms import ModelForm, CharField, Textarea, TextInput, ChoiceField, Select
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from website.models import Site
        
class KavlingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kode_kavling'].required = True
        self.fields['luas_tanah'].required = True
        self.fields['harga_per_meter'].required = True
        self.fields['harga_jual_cash'].required = False
        self.fields['map_code_path'].required = False
        
    # kode_kavling = CharField(
    #     label='Kode Kavling',
    #     widget=TextInput(attrs={'readonly': 'readonly'})
    # )
    
    map_code_path = CharField(
        label="Map Code",
        widget=Textarea(attrs={'readonly': 'readonly'})
    )
    class Meta:
        # merelasikan form dengan model
        model = Kavling
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('kode_kavling', 'luas_tanah', 'harga_per_meter', 'harga_jual_cash', 'map_code_path',)
        # mengatur teks label untuk setiap field
        labels = {
            'kode_kavling': _('Kode Kavling'),
            'luas_tanah': _('Luas Tanah'),
            'harga_per_meter': _('Harga per Meter'),
            'harga_jual_cash': _('Harga Jual Cash'),
            'map_code_path': _('Map Code'),
        }
        # mengatur teks pesan error untuk setiap validasi fieldnya
        error_messages = {
            'kode_kavling': {
                'required': _("Kode Kavling harus diisi."),
            },
            'luas_tanah': {
                'required': _("Luas Tanah harus diisi."),
            },
            'harga_per_meter': {
                'required': _("Harga per Meter harus diisi."),
            },
            'harga_jual_cash': {
                'required': _("Harga Jual Cash harus diisi."),
            },
            'map_code': {
                'required': _("Map Code harus diisi."),
            },
        }
        
class TemplateKavlingForm(ModelForm):
    class Meta:
        model = Site
        fields = ('template_kavling',)
        labels = {
            'template_kavling': _('Template Kavling'),
        }
        error_messages = {
            'template_kavling': {
                'required': _("Template Kavling harus diisi."),
            },
        }
        
class DetailKavlingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kode_kavling'].required = False
        self.fields['luas_tanah'].required = False
        self.fields['harga_jual_cash'].required = False
        
    kode_kavling = CharField(
        label='Kode Kavling',
        widget=TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'})
    )
    luas_tanah = CharField(
        label="Luas Tanah",
        widget=TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'})
    )
    harga_jual_cash = CharField(
        label="Harga Cash",
        widget=TextInput(attrs={'readonly': 'readonly', 'disabled': 'disabled'})
    )
    class Meta:
        model = Kavling
        fields = ('kode_kavling', 'luas_tanah', 'harga_jual_cash',)