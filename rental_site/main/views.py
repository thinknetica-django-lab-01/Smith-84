from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from .models import Apartment, Ad
from django.contrib.contenttypes.models import ContentType
# Create your views here.


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        turn_on_block = True
        current_user = request.user
        return render(request, self.template_name, context={'turn_on_block': turn_on_block, 'current_user': current_user})


class ApartmentAd(ListView):
    model = Ad
    template_name = 'list_ads.html'
    context_object_name = 'ads'

    def get_queryset(self):
        query = Ad.objects.filter(region__name='Абакан', action='Продажа',
                                  content_type=ContentType.objects.get_for_model(Apartment))
        return query

