from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.models import inlineformset_factory
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import *
from .forms import *
# Create your views here.


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class AdsListMixin(ListView):
    model = Ad
    template_name = 'list_ads.html'
    context_object_name = 'ads'
    realty = None
    action = None
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(ads__content_type=ContentType.objects.get_for_model(self.realty)).distinct()
        return context

    def get_queryset(self):
        data_to_query = {
            'action': self.action,
            'content_type': ContentType.objects.get_for_model(self.realty)
        }
        current_tag = self.request.GET.get('tag')
        if current_tag is not None:
            data_to_query['tag__slug'] = current_tag

        return Ad.objects.filter(**data_to_query)


class ApartmentSell(AdsListMixin):
    realty = Apartment
    action = 'sell'


class ApartmentRent(AdsListMixin):
    realty = Apartment
    action = 'rent'


class RoomSell(AdsListMixin):
    realty = Room
    action = 'sell'


class RoomRent(AdsListMixin):
    realty = Room
    action = 'rent'


class GarageSell(AdsListMixin):
    realty = Garage
    action = 'sell'


class GarageRent(AdsListMixin):
    realty = Garage
    action = 'rent'


class LandPlotSell(AdsListMixin):
    realty = LandPlot
    action = 'sell'


class AdDetail(DetailView):
    model = Ad
    template_name = 'ad_item.html'


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    second_form_class = ProfileForm
    template_name = 'profile.html'
    redirect_field_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_form = self.second_form_class(instance=self.request.user.profile)
        context['profile_form'] = profile_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.form_class(request.POST, instance=self.request.user)
        profile_form = self.second_form_class(request.POST, instance=self.request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.save()
            messages.success(request, 'Данные успешно обновлены')
        else:
            messages.error(request, 'Ошибка!')

        return self.render_to_response(self.get_context_data())


def add_realty_ad(request, **kwargs):
    all_formsets = {
        'apartment': ApartmentForm,
        'room': RoomForm,
        'garage': GarageForm,
        'land-plot': LandPlotForm
    }
    realty_type = kwargs.get('realty')
    if realty_type not in all_formsets:
        return HttpResponseNotFound('404')

    form_ad = generic_inlineformset_factory(Ad, form=AdForm, extra=1, can_delete=False)
    form_realty = all_formsets[realty_type]

    if request.method == 'POST':
        realty_form = form_realty(request.POST)
        if realty_form.is_valid():
            saved_obj = realty_form.save(commit=False)
            ad_form = form_ad(request.POST, instance=saved_obj)
            if ad_form.is_valid():
                saved_obj.save()
                ad_form.save()
            else:
                pass

        return HttpResponse('Ok')
    else:
        return render(request, 'add_new_ad.html', context={'form': form_ad, 'form2': form_realty})



class EditRealtyAd(UpdateView):
    pass
