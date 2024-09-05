from django.forms import ModelForm, DateInput, TextInput
from django.utils.translation import gettext_lazy as _
from customer.models import Customer, Galeri

class DateInput(DateInput):
    input_type = 'date'

class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tempat_lahir'].required = False
        self.fields['tanggal_lahir'].required = False
        self.fields['pekerjaan'].required = False
        self.fields['ktp'].required = False
        self.fields['kk'].required = False
        self.fields['foto_orang'].required = False
    class Meta:
        model = Customer
        fields = ('nama', 'nik', 'tempat_lahir', 'tanggal_lahir', 'no_hp', 'jk', 'alamat', 'email', 'pekerjaan', 'ktp', 'kk', 'foto_orang')
        widgets = {
            'tanggal_lahir': DateInput(),
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
            'foto_orang': _('Foto Orang')
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
        
class GaleriForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keterangan'].required = True
        self.fields['foto'].required = False
    class Meta:
        model = Galeri
        fields = ('foto','keterangan')
        labels = {
            'keterangan': _('Keterangan'),
            'foto': _('Foto')
        }
        widgets = {
            'tanggal_lahir': TextInput(),
        }
        error_messages = {
            'keterangan': {
                'required': _("Keterangan harus diisi."),
            },
            'foto': {
                'required': _("Foto harus diisi."),
            },
        }
        