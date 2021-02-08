from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.models import inlineformset_factory
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
    """
        Базовое вью списка объявлений
    """
    model = Ad
    template_name = 'list_ad.html'
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
    """
        Список объявлений квартира продажа
    """
    realty = Apartment
    action = 'sell'


class ApartmentRent(AdsListMixin):
    """
        Список объявлений квартира аренда
    """
    realty = Apartment
    action = 'rent'


class RoomSell(AdsListMixin):
    """
        Список объявлений комнаты продажа
    """
    realty = Room
    action = 'sell'


class RoomRent(AdsListMixin):
    """
        Список объявлений комнаты аренда
    """
    realty = Room
    action = 'rent'


class GarageSell(AdsListMixin):
    """
        Список объявлений гаражы продажа
    """
    realty = Garage
    action = 'sell'


class GarageRent(AdsListMixin):
    """
        Список объявлений гаражы аренда
    """
    realty = Garage
    action = 'rent'


class LandPlotSell(AdsListMixin):
    """
        Список объявлений земельных участков
    """
    realty = LandPlot
    action = 'sell'


class AdDetail(DetailView):
    """
        Страница объявления
    """
    model = Ad
    template_name = 'item_ad.html'


class Dashboard(LoginRequiredMixin, View):
    """
        Личный кабинет пользователя
    """
    def get(self, request):
        return render(request, 'dashboard.html')


class UserUpdate(LoginRequiredMixin, UpdateView):
    """
        Редактируем профиль юзера с доп формой
    """
    model = User
    form_class = UserForm
    second_form_class = ProfileForm
    template_name = 'form.html'
    redirect_field_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_form = self.second_form_class(instance=self.request.user.profile)
        context['form2'] = profile_form
        context['title'] = 'Данные профиля'
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


class RealtyList(View):
    """
        Страница с выбором - что хотим добавить
    """
    def get(self, request):
        return render(request, 'choice_type.html')


class AddRealtyAdMixin(LoginRequiredMixin, CreateView):
    """
        Базовая вью добавления объявлений
    """
    model = None
    form_class = None
    second_form_class = generic_inlineformset_factory(Ad, form=AdForm, extra=1, can_delete=False)
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.second_form_class
        return context

    def form_valid(self, form):
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
                return self.render_to_response(self.get_context_data())


class AddApartment(AddRealtyAdMixin):
    """
        Добавляем Квартиру
    """
    model = Apartment
    form_class = ApartmentForm


class AddRoom(AddRealtyAdMixin):
    """
        Добавляем комнату
    """
    model = Room
    form_class = RoomForm


class AddLandPlot(AddRealtyAdMixin):
    """
        Добавляем земельный участок
    """
    model = LandPlot
    form_class = LandPlotForm


class AddGarage(AddRealtyAdMixin):
    """
        Добавляем гараж
    """
    model = Garage
    form_class = GarageForm


class SaveImages(LoginRequiredMixin, UpdateView):
    """
        Добавление картинок к объявлению
    """
    model = Ad
    form_class = inlineformset_factory(Ad, Image, fields=('image',), extra=3, min_num=1)
    template_name = 'form_files.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        image_form = self.form_class(request.POST, request.FILES, instance=self.object)
        if image_form.is_valid():
            image_form.save()
            return redirect(reverse('ad_detail', kwargs={'slug': self.object.slug}))
        else:
            messages.error(request, 'Ошибка!')
            return self.render_to_response(self.get_context_data())


class EditRealtyAd(LoginRequiredMixin, UpdateView):
    """
        Редактирование страницы объявления
        Какую форму с доп данными подгружаем и определяем из content_type
    """
    model = Ad
    form_class = AdForm
    template_name = 'form.html'
    second_form_class = None
    form_class_sets = {
        'Квартира': ApartmentForm,
        'Комната': RoomForm,
        'Гараж': GarageForm,
        'Земельный участок': LandPlotForm
    }
    redirect_field_name = 'login.html'

    def get_second_form_class(self):
        """
            Возвращаем вторую форму в зависимости от типа объявления
        """
        return self.form_class_sets[self.object.content_type.name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.second_form_class = self.get_second_form_class()
        additional_form = self.second_form_class(instance=self.object.content_object)
        context['title'] = 'Редактирование объявления'
        context['form2'] = additional_form
        return context

    def post(self, request, *args, **kwargs):
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
            messages.error(request, 'Ошибка!')

        return self.render_to_response(self.get_context_data())
