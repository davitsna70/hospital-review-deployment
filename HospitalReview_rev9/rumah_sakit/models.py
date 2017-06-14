from django.db import models
from utama.models import Administrator, Akun, User
from django.core.urlresolvers import reverse

# Create your models here.
class RumahSakit(models.Model):
    """docstring for RumahSakit."""
    STATUS_CHOICES = (
        ('request','Request'),
        ('validated','Validated'),
        ('rejected','Rejected')
    )

    STATUS_CHOICES_KELAS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    )

    nama = models.CharField(max_length=100)
    akun = models.ForeignKey(Akun)
    foto_profil = models.ImageField(upload_to='foto_profil_rumah_sakit', blank=True)
    dokumen = models.FileField(upload_to='dokumen_rumah_sakit', blank=True)
    url_website = models.CharField(max_length=400, null=True)
    provinsi = models.CharField(max_length=100)
    kabupaten_kota = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    jalan = models.CharField(max_length=100, null=True)
    kode_pos = models.CharField(max_length=100, null=True)
    fax = models.CharField(max_length=40, null= True)
    nomor_telepon = models.CharField(max_length=20, null=True)
    lokasi_rumah_sakit_lintang = models.CharField(max_length=100, default='', null= True)
    lokasi_rumah_sakit_bujur = models.CharField(max_length=100, default='', null=True)
    status_validasi = models.CharField(max_length=20, choices=STATUS_CHOICES, default='request')
    waktu_validasi = models.DateField(blank=True, null=True)
    administrator = models.ForeignKey(Administrator,blank=True, null=True, related_name='rumah_sakits')
    kelas = models.CharField(max_length=3, choices=STATUS_CHOICES_KELAS, blank=True, null=True)

    class Meta:
        ordering = ('kelas',)

    def get_absolute_url(self):
        return reverse('rumah_sakit:rumah_sakit_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.nama

class FotoRumahSakit(models.Model):
    """docstring for FotoRumahSakit."""
    rumah_sakit = models.ForeignKey(RumahSakit, related_name='foto_rumah_sakits')
    foto_rumah_sakit = models.ImageField(upload_to='foto_rumah_sakit', blank=True)

    def get_absolute_url(self):
        return reverse('rumah_sakit:foto_rumah_sakit_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.rumah_sakit.nama

class JenisFasilitas(models.Model):
    """docstring for Fasilitas."""
    fasilitas = models.CharField(max_length=300)
    deskripsi = models.TextField()

    def get_absolute_url(self):
        return reverse('rumah_sakit:jenis_fasilitas_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.fasilitas

class FasilitasRumahSakit(models.Model):
    """docstring for FasilitasRumahSakit."""
    jenis_fasilitas = models.ForeignKey(JenisFasilitas, related_name='fasilitas_rumah_sakits')
    rumah_sakit = models.ForeignKey(RumahSakit, related_name='fasilitas_rumah_sakits')
    sub_fasilitas = models.CharField(max_length=200)
    jumlah = models.PositiveIntegerField()
    deskripsi = models.TextField()

    def get_absolute_url(self):
        return reverse('rumah_sakit:fasilitas_rumah_sakit_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.rumah_sakit.nama

class Spesialis(models.Model):
    """docstring for Spesialis."""
    jenis_spesialis = models.CharField(max_length=200)
    deskripsi = models.TextField()

    def get_absolute_url(self):
        return reverse('rumah_sakit:spesialis_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.jenis_spesialis

class Dokter(models.Model):
    """docstring for Dokter."""
    nama = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    nomor_telepon = models.CharField(max_length=20, null=True)
    rumah_sakit = models.ForeignKey(RumahSakit, related_name='dokters')
    spesialis = models.ForeignKey(Spesialis, related_name='dokters')

    def get_absolute_url(self):
        return reverse('rumah_sakit:dokter_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.nama

class JadwalDokter(models.Model):
    """docstring for JadwalDokter."""
    dokter = models.ForeignKey(Dokter, related_name='jadwal_dokters')
    senin_masuk = models.TimeField(blank=True, null=True)
    senin_keluar = models.TimeField(blank=True, null=True)
    selasa_masuk = models.TimeField(blank=True, null=True)
    selasa_keluar = models.TimeField(blank=True, null=True)
    rabu_masuk = models.TimeField(blank=True, null=True)
    rabu_keluar = models.TimeField(blank=True, null=True)
    kamis_masuk = models.TimeField(blank=True, null=True)
    kamis_keluar = models.TimeField(blank=True, null=True)
    jumat_masuk = models.TimeField(blank=True, null=True)
    jumat_keluar = models.TimeField(blank=True, null=True)
    sabtu_masuk = models.TimeField(blank=True, null=True)
    sabtu_keluar = models.TimeField(blank=True, null=True)
    minggu_masuk = models.TimeField(blank=True, null=True)
    minggu_keluar = models.TimeField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('rumah_sakit:jadwal_dokter_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.dokter.nama

class Penyakit(models.Model):
    nama = models.CharField(max_length=100)
    gejala = models.TextField()
    spesialis = models.ForeignKey(Spesialis, related_name='penyakits')

    def get_absolute_url(self):
        return reverse('rumah_sakit:penyakit_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.nama