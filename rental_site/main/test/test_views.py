from django.test import TestCase
from ..models import *
from faker import Faker
from faker import Factory
from django.contrib.auth.models import User
from ..factories import RegionFactory, GarageFactory, AdFactory, UserFactory
from django.urls import reverse

fake = Factory.create()


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



# path('accounts/', include('allauth.urls')),
# path('dashboard/', Dashboard.as_view(), name='dashboard'),
# path('dashboard/add/', RealtyList.as_view(), name='choice_type'),
# path('accounts/profile/', UserUpdate.as_view(), name='edit_user_profile'),










        # number_of_ads = 15
        # building_choices = ['new', 'second']
        # region = RegionFactory()
        # # test_user = User.objects.create_user(username=fake.username(), password=fake.password())

        # for ad in range(15):
        #     apartment_data = Apartment.objects.create(
        #         total_square=69.3,
        #         floor=5,
        #         number_of_rooms=3,
        #         kitchen_square=7.2,
        #         living_square=56,
        #         building=building_choices[0]
        #     )
        #     room_data = Room.objects.create(
        #         total_square=20,
        #         floor=3
        #     )
        #     garage_data = Garage.objects.create(
        #         total_square=20,
        #         number_of_floors=3
        #     )
        #     land_plot_data = LandPlot.objects.create(
        #         total_square=20
        #     )
        #     ad = Ad.objects.create(
        #         region=region,
        #         user=test_user,
        #         content_object=apartment_data,
        #         cost=fake.cost(),
        #         description=fake.text(),
        #         address=fake.address(),
        #         action='Продажа'
        #     )
        #     print(ad.cost)
