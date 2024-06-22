from django.forms import ModelForm, ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from website.models import *

class CustomImageFieldWidget(ClearableFileInput):
        template_name = 'backstore/widgets/image_input.html'

class SiteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = False
        self.fields['ttd'].required = False
        self.fields['no_telp'].required = False
    class Meta:
        model = Site
        fields = ('nama_website', 'nama_perusahaan', 'no_hp', 'alamat', 'email', 'no_telp', 'logo', 'ttd')
        widgets = {
            'logo': ClearableFileInput,
            'ttd': ClearableFileInput
        }
        labels = {
            'logo': _('Logo'),
            'nama_website': _('Nama Website'),
            'nama_perusahaan': _('Nama Perusahaan'),
            'no_hp': _('Nomor HP'),
            'alamat': _('Alamat'),
            'email': _('Email'),
            'no_telp': _('Nomor Telepon'),
            'ttd': _('Tanda Tangan'),
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
            'alamat': {
                'required': _("Alamat harus diisi."),
            },
            'email': {
                'required': _("Email harus diisi."),
            },
            'no_telp': {
                'required': _("Nomor Telepon harus diisi."),
            },
        }
