from django.forms import ModelForm, CharField, PasswordInput, TextInput, Textarea
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import *

# membuat class TaskForm untuk membuat task
class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields['password'].required = False
    
    password = CharField(
        label='Password',
        strip=False,
        widget=PasswordInput()
    )
        
    class Meta:
        # merelasikan form dengan model
        model = User
        # mengeset field apa saja yang akan ditampilkan pada form
        fields = ('username', 'email', 'first_name', 'last_name')
        # mengatur teks label untuk setiap field
        labels = {
            'username': _('Username'),
            'email': _('Email'),
            'first_name': _('Nama Depan'),
            'last_name': _('Nama Belakang'),
            'password': _('Password'),
        }
        # mengatur teks pesan error untuk setiap validasi fieldnya
        error_messages = {
            'username': {
                'required': _("Username harus diisi."),
            },
            'first_name': {
                'required': _("Nama Depan harus diisi."),
            },
            'last_name': {
                'required': _("Nama Belakang harus diisi."),
            },
        }
        
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
        
class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ('logo', 'nama_website', 'nama_perusahaan', 'no_hp')
        labels = {
            'logo': _('Logo'),
            'nama_website': _('Nama Website'),
            'nama_perusahaan': _('Nama Perusahaan'),
            'no_hp': _('Nomor HP'),
        }
        error_messages = {
            'logo': {
                'required': _("Logo harus diisi."),
            },
            'nama_website': {
                'required': _("Nama Website harus diisi."),
            },
            'nama_perusahaan': {
                'required': _("Nama Perusahaan harus diisi."),
            },
            'no_hp': {
                'required': _("Nomor HP harus diisi."),
            },
        }

class DateInput(forms.DateInput):
    input_type = 'date'
class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tempat_lahir'].required = False
        self.fields['tanggal_lahir'].required = False
        self.fields['pekerjaan'].required = False
        self.fields['ktp'].required = False
        self.fields['kk'].required = False
    class Meta:
        model = Customer
        fields = ('nama', 'nik', 'tempat_lahir', 'tanggal_lahir', 'no_hp', 'jk', 'alamat', 'email', 'pekerjaan', 'ktp', 'kk')
        widgets = {
            'tanggal_lahir': DateInput()
        }
        labels = {
            'nama': _('Nama'),
            'nik': _('NIK'),
            'tempat_lahir': _('Tempat Lahir'),
            'tanggal_lahir': _('Tanggal Lahir'),
            'alamat': _('Alamat'),
            'jk': _('Jenis Kelamin'),
            'no_hp': _('Nomor HP'),
            'email': _('Email'),
            'pekerjaan': _('Pekerjaan'),
            'ktp': _('KTP'),
            'kk': _('KK'),
        }
        error_messages = {
            'nama': {
                'required': _("Nama harus diisi."),
            },
            'nik': {
                'required': _("NIK harus diisi."),
            },
            'alamat': {
                'required': _("Alamat harus diisi."),
            },
            'jk': {
                'required': _("Jenis Kelamin harus diisi."),
            },
            'no_hp': {
                'required': _("Nomor HP harus diisi."),
            },
            'email': {
                'required': _("Email harus diisi."),
            },
        }
