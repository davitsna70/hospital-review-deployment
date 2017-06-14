from django.db import models
from utama.models import Administrator, Akun
from rumah_sakit.models import RumahSakit
from django.core.urlresolvers import reverse

# Create your models here.

class Asuransi(models.Model):
    """docstring for Asuransi."""
    STATUS_CHOICES = (
        ('rejected', 'Rejected'),
        ('validated', 'Validated'),
        ('request', 'Request')
    )

    akun = models.ForeignKey(Akun, related_name='asuransis')
    nama = models.CharField(max_length=100, unique=True)
    url_website = models.CharField(max_length=400)
    dokumen = models.FileField(upload_to='dokumen_asuransi', blank=True)
    foto_profil = models.ImageField(upload_to='foto_profil_asuransi', blank=True)
    nomor_telepon = models.CharField(max_length=20)
    status_validasi = models.CharField(max_length=50, choices=STATUS_CHOICES, default='request')
    waktu_validasi = models.DateTimeField(blank=True, null=True)
    administrator = models.ForeignKey(Administrator, blank=True, null=True, default=1, related_name='asuransis')

    def get_absolute_url(self):
        return reverse('asuransi:asuransi_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.nama


class HubunganRumahSakitAsuransi(models.Model):
    """docstring for HubunganRumahSakitAsuransi."""
    STATUS_CHOICES = (
        ('rejected', 'Rejected'),
        ('validated', 'Validated'),
        ('request', 'Request')
    )

    asuransi = models.ForeignKey(Asuransi, related_name='hubungan_rumah_sakit_asuransis')
    rumah_sakit = models.ForeignKey(RumahSakit, related_name='hubungan_rumah_sakit_asuransis')
    dokumen = models.FileField(upload_to='dokumen_hubungan_rumah_sakit_asuransi', blank=True)
    administrator = models.ForeignKey(Administrator, related_name='hubungan_rumah_sakit_asuransis', null=True)
    status_validasi_rumah_sakit = models.CharField(max_length=50, choices=STATUS_CHOICES, default='request')
    status_validasi_administrator = models.CharField(max_length=50, choices=STATUS_CHOICES, default='request')
    waktu_validasi = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('asuransi:hubungan_rumah_sakit_asuransi_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.rumah_sakit.nama + ' - ' + self.asuransi.nama
