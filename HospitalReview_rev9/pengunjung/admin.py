from django.contrib import admin
from .models import (Pengunjung, Review, FotoReview)

# Register your models here.

class PengunjungAdmin(admin.ModelAdmin):
    list_display = ('nama', 'akun', 'golongan_darah', 'jenis_kelamin', 'nomor_telepon')
    list_filter = ('nama', 'akun', 'golongan_darah', 'jenis_kelamin')
    search_fields = ('nama', 'akun')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pengunjung', 'rumah_sakit', 'data_lokasi_pengunjung_lintang', 'data_lokasi_pengunjung_bujur', 'status_validasi', 'rating')
    list_filter = ('pengunjung', 'rumah_sakit')
    search_fields = ('pengunjung', 'rumah_sakit')

class FotoReviewAdmin(admin.ModelAdmin):
    list_display = ('review', 'foto_review')
    list_filter = ('review', 'foto_review')
    search_fields = ('review', 'foto_review')

admin.site.register(Pengunjung, PengunjungAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FotoReview, FotoReviewAdmin)