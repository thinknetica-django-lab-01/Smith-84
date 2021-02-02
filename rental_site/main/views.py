from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

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
    second_model = Profile
    form_class = UserForm
    second_form_class = ProfileForm
    template_name = 'profile.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = self.second_form_class
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        current_user = self.model.objects.get(id=kwargs['pk'])
        profile_user = self.second_model.objects.get(user=current_user)
        form = self.form_class(request.POST, instance=current_user)
        form2 = self.second_form_class(request.POST, instance=profile_user)

        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))