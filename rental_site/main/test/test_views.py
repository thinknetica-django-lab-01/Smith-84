from django.test import TestCase
from django.urls import reverse

from main.factories import RegionFactory, GarageFactory, AdFactory, UserFactory


class IndexViewTest(TestCase):

    def test_success_index_view(self):
        self.response = self.client.get('/')
        self.assertEqual(self.response.status_code, 200)


class AdsListViewTest(TestCase):

    def test_success_apartment_sell_view(self):
        self.response = self.client.get('/sell/apartment/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_apartment_rent_view(self):
        self.response = self.client.get('/rent/apartment/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_room_sell_view(self):
        self.response = self.client.get('/sell/room/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_room_rent_view(self):
        self.response = self.client.get('/rent/room/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_garage_rent_view(self):
        self.response = self.client.get('/sell/garage/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_garage_sell_view(self):
        self.response = self.client.get('/sell/garage/')
        self.assertEqual(self.response.status_code, 200)

    def test_success_land_plot_sell_view(self):
        self.response = self.client.get('/sell/land_plot/')
        self.assertEqual(self.response.status_code, 200)


class AdDetailViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.region = RegionFactory()
        self.ad_data = GarageFactory()
        self.ad = AdFactory(region=self.region, user=self.user, content_object=self.ad_data)

    def test_success_ad_view(self):
        self.response = self.client.get(reverse('ad_detail', kwargs={'slug': self.ad.slug}))
        self.assertEqual(self.response.status_code, 200)
