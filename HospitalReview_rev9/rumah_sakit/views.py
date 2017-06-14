from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, View, ListView,
                                  DetailView, FormView, DeleteView,
                                  UpdateView, CreateView)
from .models import (Akun, RumahSakit, Administrator,
                     JadwalDokter, FotoRumahSakit, Penyakit,
                     JenisFasilitas, Dokter, Spesialis,
                     FasilitasRumahSakit)
from asuransi.models import Asuransi, HubunganRumahSakitAsuransi
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from bootstrap3_datetime.widgets import DateTimePicker
from . import form

# Create your views here.

class RumahSakitHomeView(View):
    def get(self, request):
        return render(request, 'rumah_sakit/home.html')

class RumahSakitListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'rumah_sakits'
    model = RumahSakit
    template_name = 'rumah_sakit/rumah_sakit_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (request.session['role'] != 'administrator'):
            return redirect('not_found')
        return super(RumahSakitListView, self).get(request,*args,**kwargs)

class RumahSakitCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'rumah_sakit/rumah_sakit_form.html'
    model = RumahSakit
    fields = ('nama', 'akun', 'foto_profil',
              'dokumen', 'kelas', 'url_website', 'provinsi', 'kabupaten_kota',
              'kecamatan', 'jalan', 'kode_pos', 'fax',
              'lokasi_rumah_sakit_lintang', 'lokasi_rumah_sakit_bujur',
              'nomor_telepon')

    def get(self, request, *args, **kwargs):
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(RumahSakitCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.administrator = Administrator.objects.get(pk=self.request.session['role_pk'])
        # form.instance.created_by = self.request.user
        return super(RumahSakitCreateView, self).form_valid(form)

class RumahSakitDetailView(DetailView):
    # login_url = 'utama:login'
    # redirect_field_name = ''
    model = RumahSakit
    template_name = 'rumah_sakit/rumah_sakit_detail.html'
    context_object_name = 'rumah_sakit_detail'

    def get(self, request, *args, **kwargs):
        # if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
        #     return redirect('not_found')
        # if (request.session['role'] == 'rumah_sakit' and int(kwargs[self.pk_url_kwarg]) != int(request.session['role_pk'])):
        #     return redirect('not_found')
        return super(RumahSakitDetailView, self).get(request=request, *args, **kwargs)

class RumahSakitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'rumah_sakit/rumah_sakit_form.html'
    fields = ('nama', 'akun', 'foto_profil',
              'dokumen', 'kelas', 'url_website', 'provinsi', 'kabupaten_kota',
              'kecamatan', 'jalan', 'kode_pos', 'fax',
              'lokasi_rumah_sakit_lintang', 'lokasi_rumah_sakit_bujur',
              'nomor_telepon')
    model = RumahSakit

    def get(self, request, *args, **kwargs):
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        if(request.session['role']=='rumah_sakit' and int(kwargs[self.pk_url_kwarg])!=int(request.session['role_pk'])):
            return redirect('not_found')

        return super(RumahSakitUpdateView, self).get(request=request, *args, **kwargs)

class RumahSakitDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = RumahSakit
    success_url = reverse_lazy('rumah_sakit:rumah_sakit_list')
    context_object_name = 'rumah_sakit'
    template_name = 'rumah_sakit/rumah_sakit_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if(request.session['role']!='administrator'):
            return redirect('not_found')

        return super(RumahSakitDeleteView, self).get(request=request, *args, **kwargs)

class FotoRumahSakitListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'foto_rumah_sakits'
    model = FotoRumahSakit
    template_name = 'foto_rumah_sakit/foto_rumah_sakit_list.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        if(not(request.session['status']=='validated')):
            return redirect('access_denied')
        if(request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        if(request.session['role']=='rumah_sakit'):
            self.queryset = FotoRumahSakit.objects.filter(rumah_sakit=int(request.session['role_pk']))
        return super(FotoRumahSakitListView, self).get(request, *args, **kwargs)

class FotoRumahSakitCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'foto_rumah_sakit/foto_rumah_sakit_form.html'
    model = FotoRumahSakit
    fields = ('foto_rumah_sakit',)

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(FotoRumahSakitCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.rumah_sakit = RumahSakit.objects.get(pk=int(self.request.session['role_pk']))
        return super(FotoRumahSakitCreateView, self).form_valid(form)

class FotoRumahSakitDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FotoRumahSakit
    template_name = 'foto_rumah_sakit/foto_rumah_sakit_detail.html'
    context_object_name = 'foto_rumah_sakit_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FotoRumahSakit.objects.get(
        #             rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoRumahSakitDetailView, self).get(request=request, *args, **kwargs)

class FotoRumahSakitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'foto_rumah_sakit/foto_rumah_sakit_form.html'
    fields = ('foto_rumah_sakit',)
    model = FotoRumahSakit

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FotoRumahSakit.objects.get(
        #             rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoRumahSakitUpdateView, self).get(request=request, *args, **kwargs)

class FotoRumahSakitDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FotoRumahSakit
    success_url = reverse_lazy('rumah_sakit:foto_rumah_sakit_list')
    context_object_name = 'foto_rumah_sakit'
    template_name = 'foto_rumah_sakit/foto_rumah_sakit_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FotoRumahSakit.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FotoRumahSakitDeleteView, self).get(request=request, *args, **kwargs)

class JenisFasilitasListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'jenis_fasilitass'
    model = JenisFasilitas
    template_name = 'jenis_fasilitas/jenis_fasilitas_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JenisFasilitasListView, self).get(request, *args, **kwargs)

class JenisFasilitasCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'jenis_fasilitas/jenis_fasilitas_form.html'
    model = JenisFasilitas
    fields = ('fasilitas', 'deskripsi')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JenisFasilitasCreateView, self).get(request=request, *args, **kwargs)

class JenisFasilitasDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = JenisFasilitas
    template_name = 'jenis_fasilitas/jenis_fasilitas_detail.html'
    context_object_name = 'jenis_fasilitas_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JenisFasilitasDetailView, self).get(request=request, *args, **kwargs)

class JenisFasilitasUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'jenis_fasilitas/jenis_fasilitas_form.html'
    fields = ('fasilitas', 'deskripsi')
    model = JenisFasilitas

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JenisFasilitasUpdateView, self).get(request=request, *args, **kwargs)

class JenisFasilitasDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = JenisFasilitas
    success_url = reverse_lazy('rumah_sakit:jenis_fasilitas_form')
    context_object_name = 'jenis_fasilitas'
    template_name = 'jenis_fasilitas/jenis_fasilitas_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JenisFasilitasDeleteView, self).get(request=request, *args, **kwargs)

class FasilitasRumahSakitListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'fasilitas_rumah_sakits'
    model = FasilitasRumahSakit
    template_name = 'fasilitas_rumah_sakit/fasilitas_rumah_sakit_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        if(request.session['role']=='rumah_sakit'):
            self.queryset = FasilitasRumahSakit.objects.filter(rumah_sakit=int(request.session['role_pk']))
        return super(FasilitasRumahSakitListView, self).get(request, *args, **kwargs)

class FasilitasRumahSakitCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'fasilitas_rumah_sakit/fasilitas_rumah_sakit_form.html'
    model = FasilitasRumahSakit
    fields = ('jenis_fasilitas', 'sub_fasilitas', 'jumlah', 'deskripsi')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(FasilitasRumahSakitCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.rumah_sakit = RumahSakit.objects.get(pk=int(self.request.session['role_pk']))
        return super(FasilitasRumahSakitCreateView, self).form_valid(form)

class FasilitasRumahSakitDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FasilitasRumahSakit
    template_name = 'fasilitas_rumah_sakit/fasilitas_rumah_sakit_detail.html'
    context_object_name = 'fasilitas_rumah_sakit_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FasilitasRumahSakit.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FasilitasRumahSakitDetailView, self).get(request=request, *args, **kwargs)

class FasilitasRumahSakitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'fasilitas_rumah_sakit/fasilitas_rumah_sakit_form.html'
    fields = ('sub_fasilitas', 'jumlah', 'deskripsi')
    model = FasilitasRumahSakit

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FasilitasRumahSakit.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FasilitasRumahSakitUpdateView, self).get(request=request, *args, **kwargs)

class FasilitasRumahSakitDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = FasilitasRumahSakit
    success_url = reverse_lazy('rumah_sakit:fasilitas_rumah_sakit_form')
    context_object_name = 'fasilitas_rumah_sakit'
    template_name = 'fasilitas_rumah_sakit/fasilitas_rumah_sakit_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != FasilitasRumahSakit.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(FasilitasRumahSakitDeleteView, self).get(request=request, *args, **kwargs)

class SpesialisListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'spesialiss'
    model = Spesialis
    template_name = 'spesialis/spesialis_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(SpesialisListView, self).get(request=request, *args, **kwargs)

class SpesialisCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'spesialis/spesialis_form.html'
    model = Spesialis
    fields = ('jenis_spesialis', 'deskripsi')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(SpesialisCreateView, self).get(request=request, *args, **kwargs)

class SpesialisDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Spesialis
    template_name = 'spesialis/spesialis_detail.html'
    context_object_name = 'spesialis_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(SpesialisDetailView, self).get(request=request, *args, **kwargs)

class SpesialisUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'spesialis/spesialis_form.html'
    fields = ('jenis_spesialis', 'deskripsi')
    model = Spesialis

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(SpesialisUpdateView, self).get(request=request, *args, **kwargs)

class SpesialisDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Spesialis
    success_url = reverse_lazy('rumah_sakit:spesialis_form')
    context_object_name = 'spesialis'
    template_name = 'spesialis/spesialis_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(SpesialisDeleteView, self).get(request=request, *args, **kwargs)

class DokterListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'dokters'
    model = Dokter
    template_name = 'dokter/dokter_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        if(request.session['role']=='rumah_sakit'):
            self.queryset = Dokter.objects.filter(rumah_sakit=int(request.session['role_pk']))
        return super(DokterListView, self).get(request, *args, **kwargs)

class DokterCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'dokter/dokter_form.html'
    model = Dokter
    fields = ('nama', 'email', 'nomor_telepon', 'spesialis')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit' ):
            return redirect('not_found')
        return super(DokterCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.rumah_sakit = RumahSakit.objects.get(pk=int(self.request.session['role_pk']))
        return super(DokterCreateView, self).form_valid(form)

class DokterDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Dokter
    template_name = 'dokter/dokter_detail.html'
    context_object_name = 'dokter_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != Dokter.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(DokterDetailView, self).get(request=request, *args, **kwargs)

class DokterUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'dokter/dokter_form.html'
    fields = ('nama', 'email', 'nomor_telepon', 'spesialis')
    model = Dokter

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != Dokter.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(DokterUpdateView, self).get(request=request, *args, **kwargs)

class DokterDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Dokter
    success_url = reverse_lazy('rumah_sakit:dokter_form')
    context_object_name = 'dokter'
    template_name = 'dokter/dokter_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != Dokter.objects.get(rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(DokterDeleteView, self).get(request=request, *args, **kwargs)

class JadwalDokterListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'jadwal_dokters'
    model = JadwalDokter
    template_name = 'jadwal_dokter/jadwal_dokter_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        if(request.session['role']=='rumah_sakit'):
            self.queryset = JadwalDokter.objects.filter(dokter__rumah_sakit=int(request.session['role_pk']))
        return super(JadwalDokterListView, self).get(request, *args, **kwargs)

class JadwalDokterCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'jadwal_dokter/jadwal_dokter_form.html'
    model = JadwalDokter
    fields = ( 'senin_masuk', 'senin_keluar',
              'selasa_masuk', 'selasa_keluar',
              'rabu_masuk', 'rabu_keluar',
              'kamis_masuk', 'kamis_keluar',
              'jumat_masuk', 'jumat_keluar',
              'sabtu_masuk', 'sabtu_keluar',
              'minggu_masuk', 'minggu_keluar')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(JadwalDokterCreateView, self).get(request=request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super(JadwalDokterCreateView, self).get_form(form_class)
        form.fields['senin_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                   "pickSeconds": False})
        form.fields['senin_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['selasa_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['selasa_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['rabu_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['rabu_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['kamis_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                   "pickSeconds": False})
        form.fields['kamis_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['jumat_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                   "pickSeconds": False})
        form.fields['jumat_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['sabtu_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                   "pickSeconds": False})
        form.fields['sabtu_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})
        form.fields['minggu_masuk'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                   "pickSeconds": False})
        form.fields['minggu_keluar'].widget = DateTimePicker(options={"format": "HH:mm",
                                                                    "pickSeconds": False})

        return form

    def form_valid(self, form):
        form.instance.dokter = Dokter.objects.get(pk=int(self.request.GET['id']))
        return super(JadwalDokterCreateView, self).form_valid(form)

class JadwalDokterDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = JadwalDokter
    template_name = 'jadwal_dokter/jadwal_dokter_detail.html'
    context_object_name = 'jadwal_dokter_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != JadwalDokter.objects.get(dokter__rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(JadwalDokterDetailView, self).get(request=request, *args, **kwargs)

class JadwalDokterUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'jadwal_dokter/jadwal_dokter_form.html'
    fields = ('senin_masuk', 'senin_keluar',
              'selasa_masuk', 'selasa_keluar',
              'rabu_masuk', 'rabu_keluar',
              'kamis_masuk', 'kamis_keluar',
              'jumat_masuk', 'jumat_keluar',
              'sabtu_masuk', 'sabtu_keluar',
              'minggu_masuk', 'minggu_keluar')
    model = JadwalDokter

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != JadwalDokter.objects.get(dokter__rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(JadwalDokterUpdateView, self).get(request=request, *args, **kwargs)

class JadwalDokterDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = JadwalDokter
    success_url = reverse_lazy('rumah_sakit:jadwal_dokter_form')
    context_object_name = 'jadwal_dokter'
    template_name = 'jadwal_dokter/jadwal_dokter_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'rumah_sakit'
        #         and int(kwargs[self.pk_url_kwarg]) != JadwalDokter.objects.get(dokter__rumah_sakit=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(JadwalDokterDeleteView, self).get(request=request, *args, **kwargs)

class PenyakitListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'penyakits'
    model = Penyakit
    template_name = ('penyakit/penyakit_list.html')
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(PenyakitListView, self).get(request, *args, **kwargs)

class PenyakitCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'penyakit/penyakit_form.html'
    model = Penyakit
    fields = ('nama', 'gejala', 'spesialis')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(PenyakitCreateView, self).get(request=request, *args, **kwargs)

class PenyakitDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Penyakit
    template_name = 'penyakit/penyakit_detail.html'
    context_object_name = 'penyakit_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(PenyakitDetailView, self).get(request=request, *args, **kwargs)

class PenyakitUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'penyakit/penyakit_form.html'
    fields = ('nama', 'gejala', 'spesialis')
    model = Penyakit

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(PenyakitUpdateView, self).get(request=request, *args, **kwargs)

class PenyakitDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Penyakit
    success_url = reverse_lazy('rumah_sakit:penyakit_form')
    context_object_name = 'penyakit'
    template_name = 'penyakit/penyakit_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        return super(PenyakitDeleteView, self).get(request=request, *args, **kwargs)

class AsuransiTerkaitValidatedListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'asuransis'
    model = Asuransi
    template_name = ('asuransi_terkait/asuransi_list.html')
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        self.queryset = Asuransi.objects.filter(hubungan_rumah_sakit_asuransis__rumah_sakit=int(request.session['role_pk']),
                                                hubungan_rumah_sakit_asuransis__status_validasi_rumah_sakit='validated')
        return super(AsuransiTerkaitValidatedListView, self).get(request, *args, **kwargs)

class PermintaanHubunganAsuransiListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'hubungan_rumah_sakit_asuransis'
    model = HubunganRumahSakitAsuransi
    template_name = ('asuransi_terkait/hubungan_rumah_sakit_asuransi_request_list.html')
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='rumah_sakit'):
            return redirect('not_found')
        self.queryset = HubunganRumahSakitAsuransi.objects.filter(status_validasi_rumah_sakit='request',
                                                                  rumah_sakit=int(request.session['role_pk']))
        return super(PermintaanHubunganAsuransiListView, self).get(request, *args, **kwargs)

class ValidatedHubunganAsuransiView(LoginRequiredMixin, TemplateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = ('asuransi_terkait/hubungan_rumah_sakit_asuransi_request_list.html')
    def get(self, request, *args, **kwargs):
        if(request.GET['submit'] is not None):
            hubungan_rumah_sakit_asuransi = HubunganRumahSakitAsuransi.objects.get(pk = int(request.GET['submit']))
            if (hubungan_rumah_sakit_asuransi not in HubunganRumahSakitAsuransi.objects.filter(rumah_sakit=int(request.session['role_pk']), status_validasi_rumah_sakit='request')):
                redirect('access_denied')
            hubungan_rumah_sakit_asuransi.status_validasi_rumah_sakit = 'validated'
            hubungan_rumah_sakit_asuransi.save()
            redirect('rumah_sakit:asuransi_request_list')
        return super(ValidatedHubunganAsuransiView, self).get(request, *args, **kwargs)

class RejectedHubunganAsuransiView(LoginRequiredMixin, TemplateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = ('asuransi_terkait/hubungan_rumah_sakit_asuransi_request_list.html')
    def get(self, request, *args, **kwargs):
        if(request.GET['submit'] is not None):
            hubungan_rumah_sakit_asuransi = HubunganRumahSakitAsuransi.objects.get(pk = int(request.GET['submit']))
            if (hubungan_rumah_sakit_asuransi not in HubunganRumahSakitAsuransi.objects.filter(rumah_sakit=int(request.session['role_pk']), status_validasi_rumah_sakit='request')):
                redirect('access_denied')
            hubungan_rumah_sakit_asuransi.status_validasi_rumah_sakit = 'rejected'
            hubungan_rumah_sakit_asuransi.save()
            redirect('rumah_sakit:asuransi_request_list')
        return super(RejectedHubunganAsuransiView, self).get(request, *args, **kwargs)

class RumahSakitLihatPetaView(View):
    def get(self, request, *args, **kwargs):
        if(request.GET['id'] is not None):
            id = request.GET['id']
            rumah_sakit = RumahSakit.objects.get(pk = int(id))
            bujur = rumah_sakit.lokasi_rumah_sakit_bujur
            lintang = rumah_sakit.lokasi_rumah_sakit_lintang

            return render(request, 'rumah_sakit/detail_peta.html', context={'bujur':bujur,
                                                                            'lintang':lintang})



def test(request):
    return render(request, 'test.html', {'form':form.ToDoForm()})