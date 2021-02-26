import factory
from factory.django import DjangoModelFactory
from faker import Factory
from . import signals
from .models import Garage, Ad, Region
from django.contrib.auth import get_user_model

faker = Factory.create('ru_RU')
User = get_user_model()


class RegionFactory(DjangoModelFactory):
    class Meta:
        model = Region
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: faker.city_name().format(n))


class GarageFactory(DjangoModelFactory):
    class Meta:
        model = Garage

    number_of_floors = factory.Sequence(faker.random_int)
    total_square = factory.Sequence(faker.random_int)


@factory.django.mute_signals(signals.post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: faker.email().format(n))


@factory.django.mute_signals(signals.post_save)
class AdFactory(DjangoModelFactory):
    class Meta:
        model = Ad

    region = factory.SubFactory(UserFactory)
    user = factory.SubFactory(UserFactory)
    content_object = factory.SubFactory(GarageFactory)
    cost = factory.Sequence(faker.random_int)
    description = factory.Sequence(lambda n: faker.text().format(n))
    address = factory.Sequence(lambda n: faker.street_address().format(n))
    action = faker.random_choices(elements=['sell', 'rent'])
    date_added = faker.date()
    view_count = factory.Sequence(faker.random_int)
