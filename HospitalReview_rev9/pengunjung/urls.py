from django.conf.urls import url, include
from . import views

app_name = 'pengunjung'

urlpatterns = [
    url(r'^$',views.HomeView.as_view(), name='home'),
    url(r'^pengunjung/list', views.PengunjungListView.as_view(), name='pengunjung_list'),
    url(r'^pengunjung/create', views.PengunjungCreateView.as_view(), name='pengunjung_create'),
    url(r'^pengunjung/detail/(?P<pk>\d+)/$', views.PengunjungDetailView.as_view(), name = 'pengunjung_detail'),
    url(r'^pengunjung/update/(?P<pk>\d+)/$', views.PengunjungUpdateView.as_view(), name = 'pengunjung_update'),
    url(r'^pengunjung/delete/(?P<pk>\d+)/$', views.PengunjungDeleteView.as_view(), name = 'pengunjung_delete'),
    url(r'^review/list', views.ReviewListView.as_view(), name='review_list'),
    url(r'^review/create', views.ReviewCreateView.as_view(), name='review_create'),
    url(r'^review/detail/(?P<pk>\d+)/$', views.ReviewDetailView.as_view(), name='review_detail'),
    url(r'^review/update/(?P<pk>\d+)/$', views.ReviewUpdateView.as_view(), name='review_update'),
    url(r'^review/delete/(?P<pk>\d+)/$', views.ReviewDeleteView.as_view(), name='review_delete'),
    url(r'^foto_review/list', views.FotoReviewListView.as_view(), name='foto_review_list'),
    url(r'^foto_review/create/', views.FotoReviewCreateView.as_view(), name='foto_review_create'),
    url(r'^foto_review/detail/(?P<pk>\d+)/$',views.FotoReviewDetailView.as_view(), name='foto_review_detail'),
    url(r'^foto_review/update/(?P<pk>\d+)/$',views.FotoReviewUpdateView.as_view(), name='foto_review_update'),
    url(r'^foto_review/delete/(?P<pk>\d+)/$',views.FotoReviewDeleteView.as_view(), name='foto_review_delete'),
    # url(r'^pengunjung/registrasi', views.RegistrasiAkun.as_view(), name='registrasi_pengunjung')
]