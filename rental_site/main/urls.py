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
    path('accounts/', include('allauth.urls')),


    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard/add/', RealtyList.as_view(), name='choice_type'),
    path('accounts/profile/<int:pk>/', UserUpdate.as_view(), name='edit_user_profile'),

    path('ad/add/apartment/', AddApartment.as_view(), name='add_apartment'),
    path('ad/add/room/', AddRoom.as_view(), name='add_room'),
    path('ad/add/garage/', AddGarage.as_view(), name='add_garage'),
    path('ad/add/land-plot/', AddLandPlot.as_view(), name='add_land_plot'),

    path('ad/add/photos/<uuid:pk>/', SaveImages.as_view(), name='add_image'),
    path('ad/edit/<uuid:pk>/', EditRealtyAd.as_view(), name='edit_ad'),
]
