from django.shortcuts import render, redirect
from django.views.generic import (TemplateView, View, ListView,
                                  DetailView, FormView, DeleteView,
                                  UpdateView, CreateView)
from .models import (Akun, Asuransi, Administrator,
                     RumahSakit, HubunganRumahSakitAsuransi)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'asuransi/home.html')

class AsuransiListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'asuransis'
    model = Asuransi
    template_name = 'asuransi/asuransi_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator'):
            return redirect('not_found')
        return super(AsuransiListView, self).get(request,*args,**kwargs)

class AsuransiCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'asuransi/asuransi_form.html'
    model = Asuransi
    fields = ('akun', 'nama', 'url_website',
              'dokumen', 'foto_profil', 'nomor_telepon',
              'status_validasi', 'waktu_validasi', 'administrator')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(AsuransiCreateView, self).get(request=request, *args, **kwargs)

class AsuransiDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Asuransi
    template_name = 'asuransi/asuransi_detail.html'
    context_object_name = 'asuransi_detail'

    def get(self, request, *args, **kwargs):
        if(request.session['role']!='administrator' and request.session['role']!='asuransi'):
            return redirect('not_found')
        if (request.session['role'] == 'asuransi' and int(kwargs[self.pk_url_kwarg]) != int(request.session['role_pk'])):
            return redirect('not_found')
        return super(AsuransiDetailView, self).get(request=request, *args, **kwargs)

class AsuransiUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'asuransi/asuransi_form.html'
    fields = ('nama', 'url_website',
              'dokumen', 'foto_profil', 'nomor_telepon')
    model = Asuransi

    def get(self, request, *args, **kwargs):
        if(request.session['role']!='administrator' and request.session['role']!='asuransi'):
            return redirect('not_found')
        if (request.session['role'] == 'asuransi' and int(kwargs[self.pk_url_kwarg]) != int(request.session['role_pk'])):
            return redirect('not_found')
        return super(AsuransiUpdateView, self).get(request=request, *args, **kwargs)

class AsuransiDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = Asuransi
    success_url = reverse_lazy('asuransi:asuransi_list')
    context_object_name = 'asuransi'
    template_name = 'asuransi/asuransi_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='administrator'):
            return redirect('not_found')
        return super(AsuransiDeleteView, self).get(request=request, *args, **kwargs)

class HubunganRumahSakitAsuransiListView(LoginRequiredMixin, ListView):
    login_url = 'utama:login'
    redirect_field_name = ''
    context_object_name = 'hubungan_rumah_sakit_asuransis'
    model = HubunganRumahSakitAsuransi
    template_name = 'hubungan_rumah_sakit_asuransi/hubungan_rumah_sakit_asuransi_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role']!='asuransi'):
            return redirect('not_found')
        if(request.session['role']=='asuransi'):
            self.queryset = HubunganRumahSakitAsuransi.objects.filter(asuransi=int(request.session['role_pk']))
        return super(HubunganRumahSakitAsuransiListView, self).get(request, *args, **kwargs)

class HubunganRumahSakitAsuransiCreateView(LoginRequiredMixin, CreateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'hubungan_rumah_sakit_asuransi/hubungan_rumah_sakit_asuransi_form.html'
    model = HubunganRumahSakitAsuransi
    fields = ('rumah_sakit', 'dokumen')

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if(request.session['role']!='asuransi'):
            return redirect('not_found')
        return super(HubunganRumahSakitAsuransiCreateView, self).get(request=request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.asuransi = Asuransi.objects.get(pk = self.request.session['role_pk'])
        form.instance.administrator = Administrator.objects.get(pk=1)
        form.instance.status_validasi_rumah_sakit = 'request'
        form.instance.status_validasi_administrator = 'request'
        form.instance.waktu_validasi = datetime.datetime.now()

        return super(HubunganRumahSakitAsuransiCreateView, self).form_valid(form)

class HubunganRumahSakitAsuransiDetailView(LoginRequiredMixin, DetailView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = HubunganRumahSakitAsuransi
    template_name = 'hubungan_rumah_sakit_asuransi/hubungan_rumah_sakit_asuransi_detail.html'
    context_object_name = 'hubungan_rumah_sakit_asuransi_detail'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'asuransi'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'asuransi'
        #         and int(kwargs[self.pk_url_kwarg]) != HubunganRumahSakitAsuransi.objects.get(
        #             asuransi=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(HubunganRumahSakitAsuransiDetailView, self).get(request=request, *args, **kwargs)

class HubunganRumahSakitAsuransiUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'utama:login'
    redirect_field_name = ''
    template_name = 'hubungan_rumah_sakit_asuransi/hubungan_rumah_sakit_asuransi_form.html'
    fields = ('dokumen',)
    model = HubunganRumahSakitAsuransi

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'asuransi'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'asuransi'
        #         and int(kwargs[self.pk_url_kwarg]) != HubunganRumahSakitAsuransi.objects.get(
        #             asuransi=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(HubunganRumahSakitAsuransiUpdateView, self).get(request=request, *args, **kwargs)

class HubunganRumahSakitAsuransiDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'utama:login'
    redirect_field_name = ''
    model = HubunganRumahSakitAsuransi
    success_url = reverse_lazy('asuransi:hubungan_rumah_sakit_asuransi_list')
    context_object_name = 'hubungan_rumah_sakit_asuransi'
    template_name = 'hubungan_rumah_sakit_asuransi/hubungan_rumah_sakit_asuransi_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        if (not (request.session['status'] == 'validated')):
            return redirect('access_denied')
        if (request.session['role'] != 'administrator' and request.session['role'] != 'asuransi'):
            return redirect('not_found')
        # try:
        #     if (request.session['role'] == 'asuransi'
        #         and int(kwargs[self.pk_url_kwarg]) != HubunganRumahSakitAsuransi.objects.get(
        #             asuransi=int(request.session['role_pk'])).pk):
        #         return redirect('not_found')
        # except Exception:
        #     return redirect('not_found')

        return super(HubunganRumahSakitAsuransiDeleteView, self).get(request=request, *args, **kwargs)