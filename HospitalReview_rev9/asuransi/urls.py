from django.conf.urls import url, include
from . import views

app_name = 'asuransi'

urlpatterns = [
    url(r'^$',views.HomeView.as_view(), name='home'),
    url(r'^asuransi/list', views.AsuransiListView.as_view(), name='asuransi_list'),
    url(r'^asuransi/create', views.AsuransiCreateView.as_view(), name='asuransi_create'),
    url(r'^asuransi/detail/(?P<pk>\d+)/$', views.AsuransiDetailView.as_view(), name='asuransi_detail'),
    url(r'^asuransi/update/(?P<pk>\d+)/$', views.AsuransiUpdateView.as_view(), name='asuransi_update'),
    url(r'^asuransi/delete/(?P<pk>\d+)/$', views.AsuransiDeleteView.as_view(), name='asuransi_delete'),
    url(r'^hubungan_rumah_sakit_asuransi/list', views.HubunganRumahSakitAsuransiListView.as_view(),
        name='hubungan_rumah_sakit_asuransi_list'),
    url(r'^hubungan_rumah_sakit_asuransi/create', views.HubunganRumahSakitAsuransiCreateView.as_view(),
        name='hubungan_rumah_sakit_asuransi_create'),
    url(r'^hubungan_rumah_sakit_asuransi/detail/(?P<pk>\d+)/$',views.HubunganRumahSakitAsuransiDetailView.as_view(),
        name='hubungan_rumah_sakit_asuransi_detail'),
    url(r'^hubungan_rumah_sakit_asuransi/update/(?P<pk>\d+)/$',views.HubunganRumahSakitAsuransiUpdateView.as_view(),
            name='hubungan_rumah_sakit_asuransi_update'),
    url(r'^hubungan_rumah_sakit_asuransi/delete/(?P<pk>\d+)/$',views.HubunganRumahSakitAsuransiDeleteView.as_view(),
            name='hubungan_rumah_sakit_asuransi_delete'),
]