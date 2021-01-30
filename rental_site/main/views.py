from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_list_or_404

# Create your views here.


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        turn_on_block = True
        return render(request, self.template_name, context={'turn_on_block': turn_on_block})



class AdsListMixin(ListView):
    model = Ad
    template_name = 'list_ads.html'
    context_object_name = 'ads'
    realty = None
    action = None

    def get_queryset(self):
        query = Ad.objects.filter(region__slug='abakan', action=self.action, content_type=ContentType.objects.get_for_model(self.realty))
        return query


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

