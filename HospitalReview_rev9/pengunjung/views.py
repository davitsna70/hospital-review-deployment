from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, View, ListView,
                                  DetailView, FormView, DeleteView,
                                  UpdateView, CreateView)
from .models import (RumahSakit, Akun, Review,
                     Pengunjung, FotoReview)
from utama.models import Administrator
from extra_views import InlineFormSet, CreateWithInlinesView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from function import metadata_image

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'pengunjung/home.html')

class PengunjungListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'pengunjungs'
    model = Pengunjung
    template_name = 'pengunjung/pengunjung_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='pengunjung'):
            return redirect('not_found')
        if(request.session['role']=='pengunjung'):
            self.queryset = Pengunjung.objects.filter(pk=int(request.session['role_pk']))
        return super(PengunjungListView, self).get(request,*args,**kwargs)

class PengunjungCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'pengunjung/pengunjung_form.html'
    model = Pengunjung
    fields = ('akun', 'nama', 'tempat_lahir', 'tanggal_lahir',
              'golongan_darah', 'provinsi', 'kabupaten_kota',
              'kelurahan', 'rt_rw', 'kode_pos', 'jenis_kelamin',
              'nomor_telepon', 'foto_profil')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(PengunjungCreateView, self).get(request=request, *args, **kwargs)

class PengunjungDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Pengunjung
    template_name = 'pengunjung/pengunjung_detail.html'
    context_object_name = 'pengunjung_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='pengunjung'):
            return redirect('not_found')
        if (request.session['role'] == 'pengunjung' and int(kwargs[self.pk_url_kwarg]) != int(request.session['role_pk'])):
            return redirect('not_found')
        return super(PengunjungDetailView, self).get(request=request, *args, **kwargs)

class PengunjungUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'pengunjung/pengunjung_form.html'
    fields = ('nama', 'tempat_lahir', 'tanggal_lahir',
              'golongan_darah', 'provinsi', 'kabupaten_kota',
              'kelurahan', 'rt_rw', 'kode_pos', 'jenis_kelamin',
              'nomor_telepon', 'foto_profil')
    model = Pengunjung

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='pengunjung'):
            return redirect('not_found')
        if (request.session['role'] == 'pengunjung' and int(kwargs[self.pk_url_kwarg]) != int(request.session['role_pk'])):
            return redirect('not_found')
        return super(PengunjungUpdateView, self).get(request=request, *args, **kwargs)

class PengunjungDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Pengunjung
    success_url = reverse_lazy('pengunjung:pengunjung_list')
    context_object_name = 'pengunjung'
    template_name = 'pengunjung/pengunjung_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')

        return super(PengunjungDeleteView, self).get(request=request, *args, **kwargs)

class ReviewListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'reviews'
    model = Review
    template_name = 'review/review_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='pengunjung'):
            return redirect('not_found')
        if(request.session['role']=='pengunjung'):
            self.queryset = Review.objects.filter(pengunjung=int(request.session['role_pk']))
        return super(ReviewListView, self).get(request, *args, **kwargs)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'review/review_form.html'
    model = Review
    fields = ('isi_review', 'data_lokasi_pengunjung_lintang',
              'data_lokasi_pengunjung_bujur', 'rating')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='pengunjung'):
            return redirect('not_found')
        return super(ReviewCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        if(RumahSakit.objects.filter(pk=int(self.request.GET['data'])) is None):
            raise form.ValidationError("You've been change data...")
        else:
            form.instance.rumah_sakit = RumahSakit.objects.get(pk=int(self.request.GET['data']))
            form.instance.pengunjung = Pengunjung.objects.get(pk=int(self.request.session['role_pk']))
            form.instance.waktu_validasi = datetime.datetime.now()

        return super(ReviewCreateView, self).form_valid(form)

class ReviewDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Review
    template_name = 'review/review_detail.html'
    context_object_name = 'review_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) != Review.objects.get(
        #             pengunjung=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(ReviewDetailView, self).get(request=request, *args, **kwargs)

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'review/review_form.html'
    fields = ('isi_review', 'data_lokasi_pengunjung_lintang',
              'data_lokasi_pengunjung_bujur', 'rating')
    model = Review

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) != Review.objects.get(
        #             pengunjung=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(ReviewUpdateView, self).get(request=request, *args, **kwargs)

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Review
    success_url = reverse_lazy('pengunjung:review_list')
    context_object_name = 'review'
    template_name = 'review/review_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) != Review.objects.get(
        #             pengunjung=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(ReviewDeleteView, self).get(request=request, *args, **kwargs)

class FotoReviewListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'foto_reviews'
    model = FotoReview
    template_name = 'foto_review/foto_review_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        if (request.session['role'] == 'pengunjung'):
            self.queryset = FotoReview.objects.filter(review__pengunjung=int(request.session['role_pk']))
        return super(FotoReviewListView, self).get(request, *args, **kwargs)

class FotoReviewCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'foto_review/foto_review_form.html'
    model = FotoReview
    fields = ('foto_review',)

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='pengunjung'):
            return redirect('not_found')
        return super(FotoReviewCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        if (Review.objects.filter(pk=int(self.request.GET['data'])) is None):
            raise form.ValidationError("You've been change data...")
        else:
            form.instance.review = Review.objects.get(pk=int(self.request.GET['data']))
            # print(metadata_image.get_metadata('localhost:8000/media/foto_review/IMG_20170606_182444_HrNKBSz.jpg'))
        try:
            if(metadata_image.get_metadata('G:/IMG_20170606_182444.jpg')):
                metadata = metadata_image.get_metadata('G:/IMG_20170606_182444.jpg')
                if(metadata['bujur']):
                    bujur = metadata['bujur']
                    lintang = metadata['lintang']

                    review = Review.objects.get(pk=int(self.request.GET['data']))
                    review.data_lokasi_pengunjung_bujur = bujur
                    review.data_lokasi_pengunjung_lintang = lintang
                    print(bujur)
                    print(lintang)
                    review.save()
        except:
            return super(FotoReviewCreateView, self).form_valid(form)

        return super(FotoReviewCreateView,self).form_valid(form)

class FotoReviewDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FotoReview
    template_name = 'foto_review/foto_review_detail.html'
    context_object_name = 'review_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) in FotoReview.objects.filter(
        #             review__pengunjung=int(request.session['role_pk']))):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoReviewDetailView, self).get(request=request, *args, **kwargs)

class FotoReviewUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'foto_review/foto_review_form.html'
    fields = ('review', 'foto_review')
    model = FotoReview

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) in FotoReview.objects.filter(
        #             review__pengunjung=int(request.session['role_pk']))):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoReviewUpdateView, self).get(request=request, *args, **kwargs)

class FotoReviewDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FotoReview
    success_url = reverse_lazy('pengunjung:foto_review_list')
    context_object_name = 'foto_review'
    template_name = 'foto_review/foto_review_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'pengunjung'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'pengunjung'
        #         and int(kwargs[self.pk_url_kwarg]) in FotoReview.objects.filter(
        #             review__pengunjung=int(request.session['role_pk']))):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoReviewDeleteView, self).get(request=request, *args, **kwargs)

# class RegistrasiPengunjung(InlineFormSet):
#     model = Pengunjung
#     fields = ('nama', 'tempat_lahir', 'tanggal_lahir',
#               'golongan_darah', 'alamat', 'jenis_kelamin',
#               'nomor_telepon', 'foto_profil')
#
# class RegistrasiAkun(CreateWithInlinesView):
#     template_name = 'pengunjung/registrasi_pengunjung.html'
#     inlines = [RegistrasiPengunjung]
#     model = Akun
#     fields = ('username', 'password', 'email')
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()