from rest_framework import serializers
from .models import Ad, Apartment, Room, Garage, LandPlot, Image, Tag, Region


class RegionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Region
        fields = ['id', 'name', ]


class ApartmentSerializer(serializers.HyperlinkedModelSerializer):
    # generic_data = GenericField(source='content_object', read_only=True)

    class Meta:
        model = Ad
        fields = ('description', 'cost', )
