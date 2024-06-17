from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from marketing.models import Marketing

class MarketingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['no_hp'].required = False
        self.fields['email'].required = False
    class Meta:
        model = Marketing
        fields = ('nama', 'nik', 'no_hp', 'jk', 'alamat', 'email')
        labels = {
            'nama': _('Nama'),
            'nik': _('NIK'),
            'alamat': _('Alamat'),
            'jk': _('Jenis Kelamin'),
            'no_hp': _('Nomor HP'),
            'email': _('Email'),
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
        }
        
# from marketing.models import Marketing