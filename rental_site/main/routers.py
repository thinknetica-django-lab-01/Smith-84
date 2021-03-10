from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('api/region', views.RegionViewSet)
router.register('api/apartment', views.ApartmentViewSet)