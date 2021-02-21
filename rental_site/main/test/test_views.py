from django.test import TestCase, RequestFactory
from django.urls import reverse
from main.views import Dashboard, RealtyList, AddApartment, AddRoom, AddGarage, AddLandPlot, EditRealtyAd
from main.factories import RegionFactory, GarageFactory, AdFactory, UserFactory


class IndexViewTest(TestCase):

    def test_success(self):
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

    def test_success(self):
        self.response = self.client.get(reverse('ad_detail', kwargs={'slug': self.ad.slug}))
        self.assertEqual(self.response.status_code, 200)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()

    def test_success(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user
        response = Dashboard.as_view()(request)
        self.assertEqual(response.status_code, 200)


class RealtyListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()

    def test_success(self):
        request = self.factory.get('/dashboard/add/')
        request.user = self.user
        response = RealtyList.as_view()(request)
        self.assertEqual(response.status_code, 200)


class AddRealtyAdViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()

    def test_success_add_apartment_view(self):
        request = self.factory.get('/ad/add/apartment/')
        request.user = self.user
        response = AddApartment.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_success_add_room_view(self):
        request = self.factory.get('/ad/add/room/')
        request.user = self.user
        response = AddRoom.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_success_add_garage_view(self):
        request = self.factory.get('/ad/add/garage/')
        request.user = self.user
        response = AddGarage.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_success_add_land_plot_view(self):
        request = self.factory.get('/ad/add/land-plot/')
        request.user = self.user
        response = AddLandPlot.as_view()(request)
        self.assertEqual(response.status_code, 200)


class EditRealtyAdViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.factory = RequestFactory()
        self.region = RegionFactory()
        self.ad_data = GarageFactory()
        self.ad = AdFactory(region=self.region, user=self.user, content_object=self.ad_data)

    def test_success(self):
        request = self.factory.get('/ad/add/land-plot/')
        request.user = self.user
        response = EditRealtyAd.as_view()(request, pk=self.ad.uniq_id)
        self.assertEqual(response.status_code, 200)
