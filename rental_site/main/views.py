from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
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


def add_realty_ad(request):
    form = generic_inlineformset_factory(Ad, extra=1, can_delete=False)
    if request.method == 'POST':
        pass
    else:
        pass
        # form = AddFormSet
    return render(request, 'add_new_ad.html', context={'form': form})


class EditRealtyAd(UpdateView):
    pass



#     uniq_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
#     region = models.ForeignKey(Region, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cost = models.PositiveIntegerField()
#     description = models.CharField(max_length=255, default=None)
#     address = models.CharField(max_length=200, default=None)
#     slug = models.SlugField(blank=True)
#     date_added = models.DateField(auto_now_add=True)
#     ACTION_CHOICES = [
#         ('sell', 'Продажа'),
#         ('rent', 'Аренда'),
#     ]
#     action = models.CharField(max_length=20, choices=ACTION_CHOICES)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
#         'model__in': (
#             'apartment',
#             'room',
#             'garage',
#             'landplot'
#         )
#     })
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')