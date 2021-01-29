from django.urls import path
from .views import Index, ApartmentAd

urlpatterns = [
    path('', Index.as_view()),
    path('apartment/<str>/sell/', ApartmentAd.as_view(), name='list_apartment_sell')
]
