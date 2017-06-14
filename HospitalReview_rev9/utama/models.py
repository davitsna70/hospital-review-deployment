from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse

class Akun (models.Model):
    STATUS_CHOICES = (
        ('pengunjung', 'Pengunjung'),
        ('rumah_sakit','Rumah Sakit'),
        ('asuransi', 'Asuransi'),
        ('administrator', 'Administrator')
    )
    user = models.OneToOneField(User)
    role = models.CharField(max_length=100, choices=STATUS_CHOICES)
    waktu_registrasi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Administrator(models.Model):
    STATUS_CHOICES = (
        ('pria', 'Pria'),
        ('wanita', 'Wanita')
    )

    akun = models.ForeignKey(Akun, related_name='administrators')
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    jenis_kelamin = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pria')
    nomor_telepon = models.CharField(max_length=20)
    foto_profil = models.ImageField(upload_to='foto_profil_administrator', blank=True)

    def __str__(self):
        return self.nama

    def get_absolute_url(self):
        return reverse('utama:administrator_detail', kwargs={'pk':self.pk})

class Berita(models.Model):
    judul = models.CharField(max_length=200, unique=True)
    isi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)
    administrator = models.ForeignKey(Administrator, related_name='beritas')
    foto_berita = models.ImageField(upload_to='foto_berita', blank=True)

    class Meta:
        ordering = ('-waktu',)

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('utama:detail', kwargs={'pk':self.pk})

class Pesan(models.Model):
    akun = models.ForeignKey(Akun, related_name='pesans')
    judul = models.CharField(max_length=200)
    isi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-waktu',)

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('utama:pesan_detail', kwargs={'pk':self.pk})
