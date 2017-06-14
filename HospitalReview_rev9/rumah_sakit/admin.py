from django.contrib import admin
from .models import (RumahSakit, FotoRumahSakit, JenisFasilitas,
                     FasilitasRumahSakit, Spesialis, Dokter,
                     JadwalDokter, Penyakit)
# Register your models here.

class RumahSakitAdmin(admin.ModelAdmin):
    list_display = ('nama', 'akun', 'kelas', 'url_website', 'nomor_telepon', 'fax', 'lokasi_rumah_sakit_lintang', 'lokasi_rumah_sakit_bujur', 'dokumen', 'status_validasi')
    list_filter = ('nama', 'akun', 'kelas')
    search_fields = ('nama','akun')

class FotoRumahSakitAdmin(admin.ModelAdmin):
    list_display = ('rumah_sakit', 'foto_rumah_sakit')
    list_filter = ('rumah_sakit', 'foto_rumah_sakit')
    search_fields = ('rumah_sakit', 'foto_rumah_sakit')

class FasilitasRumahSakitAdmin(admin.ModelAdmin):
    list_display = ('jenis_fasilitas', 'rumah_sakit', 'sub_fasilitas', 'jumlah')
    list_filter = ('jenis_fasilitas', 'rumah_sakit', 'sub_fasilitas')
    search_fields = ('jenis_fasilitas', 'rumah_sakit', 'sub_fasilitas')

class DokterAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'nomor_telepon', 'rumah_sakit', 'spesialis')
    list_filter = ('nama', 'email', 'rumah_sakit', 'spesialis')
    search_fields = ('nama', 'email', 'rumah_sakit', 'spesialis')

class PenyakitAdmin(admin.ModelAdmin):
    list_display = ('nama', 'spesialis')
    list_filter = ('nama', 'spesialis')
    search_fields = ('nama', 'spesialis')

admin.site.register(RumahSakit, RumahSakitAdmin)
admin.site.register(FotoRumahSakit, FotoRumahSakitAdmin)
admin.site.register(JenisFasilitas)
admin.site.register(FasilitasRumahSakit, FasilitasRumahSakitAdmin)
admin.site.register(Spesialis)
admin.site.register(Dokter, DokterAdmin)
admin.site.register(JadwalDokter)
admin.site.register(Penyakit, PenyakitAdmin)