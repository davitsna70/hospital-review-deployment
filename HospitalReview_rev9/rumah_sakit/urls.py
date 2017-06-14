from django.conf.urls import url, include
from . import views

app_name = 'rumah_sakit'

urlpatterns = [
    url(r'^$',views.RumahSakitHomeView.as_view(), name='home'),
    url(r'^rumah_sakit/list', views.RumahSakitListView.as_view(), name='rumah_sakit_list'),
    url(r'^rumah_sakit/create',views.RumahSakitCreateView.as_view(), name='rumah_sakit_create'),
    url(r'^rumah_sakit/detail/(?P<pk>\d+)/$',views.RumahSakitDetailView.as_view(), name='rumah_sakit_detail'),
    url(r'^rumah_sakit/detail/peta',views.RumahSakitLihatPetaView.as_view(), name='lihat_peta_rumah_sakit'),
    url(r'^rumah_sakit/update/(?P<pk>\d+)/$',views.RumahSakitUpdateView.as_view(), name='rumah_sakit_update'),
    url(r'^rumah_sakit/delete/(?P<pk>\d+)/$',views.RumahSakitDeleteView.as_view(), name='rumah_sakit_delete'),

    url(r'^foto_rumah_sakit/list', views.FotoRumahSakitListView.as_view(), name='foto_rumah_sakit_list'),
    url(r'^foto_rumah_sakit/create', views.FotoRumahSakitCreateView.as_view(), name='foto_rumah_sakit_create'),
    url(r'^foto_rumah_sakit/detail/(?P<pk>\d+)/$', views.FotoRumahSakitDetailView.as_view(), name='foto_rumah_sakit_detail'),
    url(r'^foto_rumah_sakit/update/(?P<pk>\d+)/$', views.FotoRumahSakitUpdateView.as_view(), name='foto_rumah_sakit_update'),
    url(r'^foto_rumah_sakit/delete/(?P<pk>\d+)/$', views.FotoRumahSakitDeleteView.as_view(), name='foto_rumah_sakit_delete'),

    url(r'^jenis_fasilitas/list',views.JenisFasilitasListView.as_view(), name='jenis_fasilitas_list'),
    url(r'^jenis_fasilitas/create',views.JenisFasilitasCreateView.as_view(), name='jenis_fasilitas_create'),
    url(r'^jenis_fasilitas/detail/(?P<pk>\d+)/$', views.JenisFasilitasDetailView.as_view(), name='jenis_fasilitas_detail'),
    url(r'^jenis_fasilitas/update/(?P<pk>\d+)/$', views.JenisFasilitasUpdateView.as_view(), name='jenis_fasilitas_update'),
    url(r'^jenis_fasilitas/delete/(?P<pk>\d+)/$', views.JenisFasilitasDeleteView.as_view(), name='jenis_fasilitas_delete'),

    url(r'^fasilitas_rumah_sakit/list', views.FasilitasRumahSakitListView.as_view(), name='fasilitas_rumah_sakit_list'),
    url(r'^fasilitas_rumah_sakit/create', views.FasilitasRumahSakitCreateView.as_view(), name='fasilitas_rumah_sakit_create'),
    url(r'^fasilitas_rumah_sakit/detail/(?P<pk>\d+)/$', views.FasilitasRumahSakitDetailView.as_view(), name='fasilitas_rumah_sakit_detail'),
    url(r'^fasilitas_rumah_sakit/update/(?P<pk>\d+)/$', views.FasilitasRumahSakitUpdateView.as_view(), name='fasilitas_rumah_sakit_update'),
    url(r'^fasilitas_rumah_sakit/delete/(?P<pk>\d+)/$', views.FasilitasRumahSakitDeleteView.as_view(), name='fasilitas_rumah_sakit_delete'),

    url(r'^spesialis/list', views.SpesialisListView.as_view(), name='spesialis_list'),
    url(r'^spesialis/create', views.SpesialisCreateView.as_view(), name='spesialis_create'),
    url(r'^spesialis/detail/(?P<pk>\d+)/$', views.SpesialisDetailView.as_view(), name='spesialis_detail'),
    url(r'^spesialis/update/(?P<pk>\d+)/$', views.SpesialisUpdateView.as_view(), name='spesialis_update'),
    url(r'^spesialis/delete/(?P<pk>\d+)/$', views.SpesialisDeleteView.as_view(), name='spesialis_delete'),

    url(r'^dokter/list', views.DokterListView.as_view(), name='dokter_list'),
    url(r'^dokter/create', views.DokterCreateView.as_view(), name='dokter_create'),
    url(r'^dokter/detail/(?P<pk>\d+)/$', views.DokterDetailView.as_view(), name='dokter_detail'),
    url(r'^dokter/update/(?P<pk>\d+)/$', views.DokterUpdateView.as_view(), name='dokter_update'),
    url(r'^dokter/delete/(?P<pk>\d+)/$', views.DokterDeleteView.as_view(), name='dokter_delete'),

    url(r'^jadwal_dokter/list', views.JadwalDokterListView.as_view(), name='jadwal_dokter_list'),
    url(r'^jadwal_dokter/create', views.JadwalDokterCreateView.as_view(), name='jadwal_dokter_create'),
    url(r'^jadwal_dokter/detail/(?P<pk>\d+)/$', views.JadwalDokterDetailView.as_view(), name='jadwal_dokter_detail'),
    url(r'^jadwal_dokter/update/(?P<pk>\d+)/$', views.JadwalDokterUpdateView.as_view(), name='jadwal_dokter_update'),
    url(r'^jadwal_dokter/delete/(?P<pk>\d+)/$', views.JadwalDokterDeleteView.as_view(), name='jadwal_dokter_delete'),

    url(r'^penyakit/list', views.PenyakitListView.as_view(), name='penyakit_list'),
    url(r'^penyakit/create', views.PenyakitCreateView.as_view(), name='penyakit_create'),
    url(r'^penyakit/detail/(?P<pk>\d+)/$', views.PenyakitDetailView.as_view(), name='penyakit_detail'),
    url(r'^penyakit/update/(?P<pk>\d+)/$', views.PenyakitUpdateView.as_view(), name='penyakit_update'),
    url(r'^penyakit/delete/(?P<pk>\d+)/$', views.PenyakitDeleteView.as_view(), name='penyakit_delete'),

    url(r'^asuransi/validated/list', views.AsuransiTerkaitValidatedListView.as_view(), name='asuransi_validated_list'),
    url(r'^asuransi/request/list', views.PermintaanHubunganAsuransiListView.as_view(), name='asuransi_request_list'),
    url(r'^asuransi/validated/$',views.ValidatedHubunganAsuransiView.as_view(), name='validated_hubungan_asuransi_by_rumah_sakit'),
    url(r'^asuransi/rejected/$',views.RejectedHubunganAsuransiView.as_view(), name='rejected_hubungan_asuransi_by_rumah_sakit'),

    url(r'^test', views.test, name='test'),
]