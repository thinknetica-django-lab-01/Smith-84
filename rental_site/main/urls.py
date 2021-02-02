from django.urls import path
from .views import *

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
    path('accounts/profile/<int:pk>/', UserUpdate.as_view(), name='user_profile'),
]