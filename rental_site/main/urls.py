from . import views
from django.urls import path
from django.urls import include
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from .models import Ad
from rest_framework import routers

ads_dict = {
    'queryset': Ad.objects.all(),
    'date_field': 'date_added',
}

router = routers.DefaultRouter()


urlpatterns = [
    path('', views.Index.as_view()),
    path('sell/apartment/', views.ApartmentSell.as_view(), name='apartment_sell'),
    path('sell/room/', views.RoomSell.as_view(), name='room_sell'),
    path('sell/garage/', views.GarageSell.as_view(), name='garage_sell'),
    path('sell/land_plot/', views.LandPlotSell.as_view(), name='land_plot_sell'),
    path('rent/apartment/', views.ApartmentRent.as_view(), name='apartment_rent'),
    path('rent/room/', views.RoomRent.as_view(), name='room_rent'),
    path('rent/garage/', views.GarageRent.as_view(), name='garage_rent'),
    path('ad/<str:slug>/', views.AdDetail.as_view(), name='ad_detail'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/add/', views.RealtyList.as_view(), name='choice_type'),
    path('accounts/profile/', views.UserUpdate.as_view(), name='edit_user_profile'),
    path('ad/add/apartment/', views.AddApartment.as_view(), name='add_apartment'),
    path('ad/add/room/', views.AddRoom.as_view(), name='add_room'),
    path('ad/add/garage/', views.AddGarage.as_view(), name='add_garage'),
    path('ad/add/land-plot/', views.AddLandPlot.as_view(), name='add_land_plot'),
    path('ad/add/photos/<uuid:pk>/', views.SaveImages.as_view(), name='add_image'),
    path('ad/edit/<uuid:pk>/', views.EditRealtyAd.as_view(), name='edit_ad'),
    path('search/', views.SearchAd.as_view(), name='search_ad'),
    path('sitemap.xml', sitemap, {'sitemaps': {'rental_site': GenericSitemap(ads_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", views.robots_txt),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
