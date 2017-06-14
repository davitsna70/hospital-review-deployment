from django.contrib import admin
from .models import (Akun, Administrator, Berita, Pesan)

# Register your models here.

class AkunAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'waktu_registrasi')
    list_filter = ('user', 'role', 'waktu_registrasi')
    search_fields = ('user', 'role', 'waktu_registrasi')

class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('akun', 'nama', 'jenis_kelamin', 'nomor_telepon')
    list_filter = ('akun', 'nama', 'jenis_kelamin', 'nomor_telepon')
    search_fields = ('akun', 'nama', 'nomor_telepon')

class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'waktu', 'administrator')
    list_filter = ('judul', 'waktu')
    search_fields = ('judul', 'waktu')

admin.site.register(Akun, AkunAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Berita, BeritaAdmin)
admin.site.register(Pesan)