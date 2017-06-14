from django.db import models
from utama.models import Akun
from rumah_sakit.models import (RumahSakit)
from django.core.urlresolvers import reverse

# Create your models here.
class Pengunjung(models.Model):
    """docstring for User."""
    STATUS_CHOICES = (
        ('pria','Pria'),
        ('wanita','Wanita')
    )

    VALIDASI_CHOICES = (
        ('request', 'Request'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected')
    )

    GOLONGAN_DARAH_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    )

    nama = models.CharField(max_length=100)
    akun = models.ForeignKey(Akun, related_name='pengunjungs')
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    golongan_darah = models.CharField(max_length=4, choices=GOLONGAN_DARAH_CHOICES, default='A+')
    provinsi = models.CharField(max_length=100, null=True)
    kabupaten_kota = models.CharField(max_length=100, null=True)
    kecamatan = models.CharField(max_length=100, null=True)
    kelurahan = models.CharField(max_length=100, null=True)
    rt_rw = models.CharField(max_length=100, null=True)
    kode_pos = models.CharField(max_length=40, null=True)
    jenis_kelamin = models.CharField(max_length=8, choices=STATUS_CHOICES, default='jenis')
    nomor_telepon = models.CharField(max_length=20, null=True)
    foto_profil = models.ImageField(upload_to='foto_profil_pengunjung', blank=True)
    status_validasi = models.CharField(max_length=30, choices=VALIDASI_CHOICES, default='request')

    def get_absolute_url(self):
        return reverse('pengunjung:pengunjung_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.nama

class Review(models.Model):
    """docstring for Review."""
    STATUS_CHOICES = (
        ('rejected','Rejected'),
        ('validated','Validated'),
        ('request','Request'),
        ('rejected_by_system','Rejected By System')
    )

    pengunjung = models.ForeignKey(Pengunjung, related_name='reviews')
    rumah_sakit = models.ForeignKey(RumahSakit, related_name='reviews')
    isi_review = models.TextField()
    waktu_stamp = models.DateTimeField(auto_now_add=True)
    waktu_validasi = models.DateTimeField(blank=True, null=True)
    data_lokasi_pengunjung_lintang = models.CharField(max_length=300, null=True, default='')
    data_lokasi_pengunjung_bujur = models.CharField(max_length=300, null=True, default='')
    status_validasi = models.CharField(max_length=50, choices=STATUS_CHOICES, default='request')
    rating = models.PositiveIntegerField()

    def get_absolute_url(self):
        return reverse('pengunjung:review_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.pengunjung)

class FotoReview(models.Model):
    """docstring for FotoReview."""
    review = models.ForeignKey(Review, related_name='foto_reviews')
    foto_review = models.ImageField(upload_to='foto_review', blank=True)

    def get_absolute_url(self):
        return reverse('pengunjung:foto_review_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.review.pengunjung.nama

