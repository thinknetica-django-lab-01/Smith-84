from django.urls import path
from .views import *
from django.urls import include

urlpatterns = [
    path('', Index.as_view()),
    path('sell/apartment/', ApartmentSell.as_view(), name='apartment_sell'),
    path('sell/room/', RoomSell.as_view(), name='room_sell'),
    path('sell/garage/', GarageSell.as_view(), name='garage_sell'),
    path('sell/land_plot/', LandPlotSell.as_view(), name='land_plot_sell'),
    path('rent/apartment/', ApartmentRent.as_view(), name='apartment_rent'),
    path('rent/room/', RoomRent.as_view(), name='room_rent'),
    path('rent/garage/', GarageRent.as_view(), name='garage_rent'),
    path('ad/<str:slug>/', AdDetail.as_view(), name='ad_detail'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('ad/add/<str:realty>/', add_realty_ad, name='add_new_ad'),
    path('ad/edit/<str:pk>/', EditRealtyAd.as_view(), name='edit_ad'),



    path('accounts/profile/<int:pk>/', UserUpdate.as_view(), name='user_profile'),

]
