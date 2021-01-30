from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from .models import Apartment, Ad, Region
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_list_or_404

# Create your views here.


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        turn_on_block = True
        return render(request, self.template_name, context={'turn_on_block': turn_on_block})


class AdsList(ListView):
    model = Ad
    template_name = 'list_ads.html'
    context_object_name = 'ads'

    # def get(self, *args, **kwargs):
    #     pass
        # resp = super().get(*args, **kwargs)
        # if Region.objects.filter(name=kwargs['str']).exists():
        #     print(kwargs['str'])
        # return resp

    def get_queryset(self, *args, **kwargs):
        print(self.request)
        print(args)
        print(kwargs)
        query = Ad.objects.filter(region__name='Абакан', action='Продажа', content_type=ContentType.objects.get_for_model(Apartment))
        return query

