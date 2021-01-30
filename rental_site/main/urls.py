from django.urls import path
from .views import Index, AdsList

urlpatterns = [
    path('', Index.as_view()),
    path('sell/apartment/', AdsList.as_view(), name='apartment_sell'),
    path('sell/room/', AdsList.as_view(), name='room_sell'),
    path('sell/garage/', AdsList.as_view(), name='garage_sell'),
    path('sell/land_plot/', AdsList.as_view(), name='land_plot_sell'),
    path('rent/apartment/', AdsList.as_view(), name='apartment_rent'),
    path('rent/room/', AdsList.as_view(), name='room_rent'),
    path('rent/garage/', AdsList.as_view(), name='garage_rent')
]