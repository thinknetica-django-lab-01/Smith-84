from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, AnonymousUser
from .models import Ad, Apartment, Room, Garage, LandPlot, Image, Tag
from .forms import AdForm, RoomForm, ApartmentForm, GarageForm, LandPlotForm
from .forms import SubscribersForm, SearchApartmentForm, UserForm, ProfileForm
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from typing import Dict, Any, Union, Type


# Create your views here.


class Index(View):
    """
        Класс-представление основной страницы
    """
    template_name = 'index.html'
    sub_form = SubscribersForm
    search_form = SearchApartmentForm

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, context={'sub_form': self.sub_form, 'search_form': self.search_form})

    def post(self, request: HttpRequest) -> HttpResponse:
        fill_form = self.sub_form(request.POST)
        if fill_form.is_valid():
            fill_form.save()
            messages.success(request, 'Вы подписались на рассылку!')
        else:
            messages.error(request, f'Ошибка! {fill_form.errors.as_text()} ')

        return render(request, self.template_name, context={'sub_form': self.sub_form})


class AdsListMixin(ListView):
    """
        Базовый класс-представление списка объявлений
    """
    model = Ad
    template_name = 'list_ad.html'
    context_object_name = 'ads'
    realty = None
    action = None
    paginate_by = 10

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.filter(
            ads__content_type=ContentType.objects.get_for_model(self.realty)).distinct()
        return context

    def get_queryset(self) -> 'QuerySet[Ad]':
        data_to_query = {
            'action': self.action,
            'content_type': ContentType.objects.get_for_model(self.realty)
        }
        current_tag = self.request.GET.get('tag')
        if current_tag is not None:
            data_to_query['tag__slug'] = current_tag

        return Ad.objects.filter(**data_to_query)


class ApartmentSell(AdsListMixin):
    """
        Класс-представление списка объявлений квартир для продажы
    """
    realty = Apartment
    action = 'sell'


class ApartmentRent(AdsListMixin):
    """
        Класс-представление списка объявлений квартир для аренды
    """
    realty = Apartment
    action = 'rent'


class RoomSell(AdsListMixin):
    """
        Класс-представление списка объявлений комнат для продажы
    """
    realty = Room
    action = 'sell'


class RoomRent(AdsListMixin):
    """
        Класс-представление списка объявлений комнат для аренды
    """
    realty = Room
    action = 'rent'


class GarageSell(AdsListMixin):
    """
        Класс-представление списка объявлений гаражей для продажы
    """
    realty = Garage
    action = 'sell'


class GarageRent(AdsListMixin):
    """
        Класс-представление списка объявлений гаражей для аренды
    """
    realty = Garage
    action = 'rent'


class LandPlotSell(AdsListMixin):
    """
        Класс-представление списка объявлений земельных участков
    """
    realty = LandPlot
    action = 'sell'


# @method_decorator(cache_page(60 * 5), name='dispatch')
class AdDetail(DetailView):
    """
        Класс-представление страницы объявления
    """
    model = Ad
    template_name = 'item_ad.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.object.view_count += 1
        self.object.save()
        key = f'{self.object.pk}_counter'
        counter = cache.get(key)
        if counter is None:
            counter = self.object.view_count
            cache.set(key, counter, 60)
        context['counter'] = counter
        return context


class Dashboard(LoginRequiredMixin, View):
    """
        Класс-представление страницы кабинета пользователя
    """
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'dashboard.html')


class UserUpdate(LoginRequiredMixin, UpdateView):
    """
        Класс-представление страницы для редактирования профиля пользователя
    """
    model = User
    form_class = UserForm
    second_form_class = ProfileForm
    template_name = 'form.html'
    redirect_field_name = 'accounts/login/'

    def get_object(self, *args, **kwargs) -> Union[User, AnonymousUser]:
        return self.request.user

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile_form = self.second_form_class(instance=self.request.user.profile)
        context['additional_form'] = profile_form
        context['title'] = 'Данные профиля'
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
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
            messages.error(request, f'Ошибка! {profile_form.errors.as_text()} {user_form.errors.as_text()} ')

        return self.render_to_response(self.get_context_data())


class RealtyList(LoginRequiredMixin, View):
    """
        Класс-представление страницы выбора типа объявления которые пользователь
         может добавить
    """
    login_url = '/accounts/signup/'
    redirect_field_name = 'redirect_to'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'choice_type.html')


class AddRealtyAdMixin(LoginRequiredMixin, CreateView):
    """
        Базовый класс-представление страницы добавления объявления
    """
    model = None
    form_class = None
    second_form_class = generic_inlineformset_factory(Ad, form=AdForm, extra=1, can_delete=False)
    template_name = 'form.html'
    redirect_field_name = 'accounts/login/'
    permission_required = 'main.add_ad'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['additional_form'] = self.second_form_class
        return context

    def form_valid(self, form) -> Union[HttpResponse, HttpResponseRedirect]:
        if form.is_valid():
            obj = form.save(commit=False)
            ad_form = self.second_form_class(data=self.request.POST, instance=obj)
            if ad_form.is_valid():
                obj.save()
                ad_pk = None
                ad_obj = ad_form.save(commit=False)
                for ad in ad_obj:
                    ad.user = self.request.user
                    ad_pk = ad.uniq_id
                    ad.save()
                return redirect(reverse('add_image', args=[ad_pk]))
            else:
                messages.error(self.request, f'Ошибка! {ad_form.errors.as_text()}')
        return self.render_to_response(self.get_context_data())


class AddApartment(AddRealtyAdMixin):
    """
        Класс-представление страницы добавляния объявления типа квартира
    """
    model = Apartment
    form_class = ApartmentForm


class AddRoom(AddRealtyAdMixin):
    """
        Класс-представление страницы добавляния объявления типа комнаты
    """
    model = Room
    form_class = RoomForm


class AddLandPlot(AddRealtyAdMixin):
    """
        Класс-представление страницы добавляния объявления типа земельный участок
    """
    model = LandPlot
    form_class = LandPlotForm


class AddGarage(AddRealtyAdMixin):
    """
        Класс-представление страницы добавляния объявления типа гараж
    """
    model = Garage
    form_class = GarageForm


class SaveImages(PermissionRequiredMixin, UpdateView):
    """
        Класс-представление страницы добавление картинок к объявлению
    """
    model = Ad
    form_class = inlineformset_factory(Ad, Image, fields=('image',), extra=3, min_num=1)
    template_name = 'form_files.html'
    redirect_field_name = 'accounts/login/'
    permission_required = 'main.change_ad'

    def post(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        self.object = self.get_object()
        image_formset = self.form_class(request.POST, request.FILES, instance=self.object)
        if image_formset.is_valid():
            image_formset.save()
            return redirect(reverse('ad_detail', kwargs={'slug': self.object.slug}))
        else:
            messages.error(request, 'Ошибка! Загрузите изображение!')
            return self.render_to_response(self.get_context_data())


class EditRealtyAd(PermissionRequiredMixin, UpdateView):
    """
        Класс-представление страницы редактирования объявления
    """
    model = Ad
    form_class = AdForm
    template_name = 'form.html'
    second_form_class = None
    form_class_sets = {
        'Apartment': ApartmentForm,
        'Room': RoomForm,
        'Garage': GarageForm,
        'LandPlot': LandPlotForm
    }
    redirect_field_name = 'accounts/login/'
    permission_required = 'main.change_ad'

    def get_second_form_class(self) -> Type[Union[ApartmentForm, RoomForm, GarageForm, LandPlotForm]]:
        """
            Метод который возвращает вторую форму в зависимости от типа объявления
        """
        return self.form_class_sets[self.object.content_type.model_class().__name__]

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.second_form_class = self.get_second_form_class()
        additional_form = self.second_form_class(instance=self.object.content_object)
        context['title'] = 'Редактирование объявления'
        context['additional_form'] = additional_form
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        ad_form = self.form_class(request.POST, instance=self.object)
        self.second_form_class = self.get_second_form_class()
        additional_form = self.second_form_class(request.POST, instance=self.object.content_object)

        if ad_form.is_valid() and additional_form.is_valid():
            ad = ad_form.save(commit=False)
            ad.save()
            additional = additional_form.save(commit=False)
            additional.save()
            messages.success(request, 'Данные успешно обновлены')
        else:
            messages.error(request, f'Ошибка! {ad_form.errors.as_text()}')

        return self.render_to_response(self.get_context_data())
