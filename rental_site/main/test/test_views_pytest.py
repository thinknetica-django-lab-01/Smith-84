import pytest
from django.urls import reverse
from main.factories import RegionFactory, GarageFactory, AdFactory, UserFactory


@pytest.mark.django_db
def test_success_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_apartment_sell_view(client):
    url = reverse('apartment_sell')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_apartment_rent_view(client):
    url = reverse('apartment_rent')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_room_sell_view(client):
    url = reverse('room_sell')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_room_rent_view(client):
    url = reverse('room_rent')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_garage_rent_view(client):
    url = reverse('garage_rent')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_garage_sell_view(client):
    url = reverse('garage_sell')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_land_plot_sell_view(client):
    url = reverse('land_plot_sell')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_ad_view(client):
    user = UserFactory()
    region = RegionFactory()
    ad_data = GarageFactory()
    ad = AdFactory(region=region, user=user, content_object=ad_data)
    url = reverse('ad_detail', kwargs={'slug': ad.slug})
    response = client.get(url)
    assert response.status_code == 200


# https://djangostars.com/blog/django-pytest-testing/
