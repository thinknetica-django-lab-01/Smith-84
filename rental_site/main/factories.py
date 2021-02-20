import factory
from .models import *
from factory.django import DjangoModelFactory
from faker import Factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

faker = Factory.create('ru_RU')
User = get_user_model()


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region

    name = faker.city_name()


class GarageFactory(DjangoModelFactory):
    class Meta:
        model = Garage

    number_of_floors = faker.random_int()
    total_square = faker.random_int()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = faker.email()


class AdFactory(DjangoModelFactory):
    class Meta:
        model = Ad

    region = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(GarageFactory)
    cost = faker.random_int()
    description = faker.text()
    address = faker.street_address()
    action = 'Продажа'
    date_added = faker.random_int()
    view_count = faker.random_int()