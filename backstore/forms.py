from django.forms import ModelForm, CharField, PasswordInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

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