from django import forms
from utama.models import Administrator, Akun
from pengunjung.models import Pengunjung
from asuransi.models import Asuransi
from rumah_sakit.models import RumahSakit
from django.contrib.auth.models import User
from bootstrap3_datetime.widgets import DateTimeInput, DateTimePicker
from datetimewidget.widgets import DateTimeWidget


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username','email', 'password')

class AdministratorForm(forms.ModelForm):
    class Meta():
        model = Administrator
        fields = ('nama', 'jenis_kelamin', 'nomor_telepon', 'foto_profil')

class PengunjungForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    class Meta():
        model = Pengunjung
        fields = ('nama', 'tempat_lahir',
                  'tanggal_lahir', 'golongan_darah', 'provinsi',
                  'kabupaten_kota', 'kecamatan', 'kelurahan',
                  'rt_rw', 'kode_pos',
                  'jenis_kelamin', 'nomor_telepon', 'foto_profil')

class AsuransiForm(forms.ModelForm):
    class Meta():
        model = Asuransi
        fields = ('nama', 'url_website',
                  'foto_profil', 'dokumen', 'nomor_telepon') ##

class RumahSakitForm(forms.ModelForm):
    class Meta():
        model = RumahSakit
        fields = ('nama', 'foto_profil', 'dokumen', 'kelas',
                  'url_website', 'provinsi', 'kabupaten_kota',
                  'kecamatan', 'jalan', 'kelas', 'kode_pos', 'fax',
                  'lokasi_rumah_sakit_lintang',
                  'lokasi_rumah_sakit_bujur', 'nomor_telepon')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # authenticate(username=username, password=password)
        # akun_qs = Akun.objects.filter(username=username)
        #
        # if not akun_qs.count()>=1:
        #     raise forms.ValidationError("account is not exist")
        # else:
        #     akun = akun_qs.first()
        # if not (akun.password == password):
        #     raise forms.ValidationError("username and password is not match")

        return super(UserLoginForm, self).clean()