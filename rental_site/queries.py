from .main.models import *

new_city_1 = Region(name='Абакан')
new_city_1.save()

new_city_2 = Region(name='Саяногорск')
new_city_2.save()

john = User.objects.create_user('johnny', 'john@gmail.com', '123123123j')
dan = User.objects.create_user('dan', 'john@gmail.com', '123123123j')

john_profile = Profile.objects.create(user=john, phone_number='+79095696363')
dan_profile = Profile.objects.create(user=dan, phone_number='+79095696362')

new_ad_data = {'cost': 1000, 'description': 'Отличная квартира', 'address': '11 микрорайон', 'action': 'Продажа'}
apartment_data = Apartment.objects.create(total_square=69.3, floor=5, number_of_rooms=3, kitchen_square=7.2, living_square=56)
new_ad = Ad.objects.create(region=new_city_1, user=john, content_object=apartment_data, **new_ad_data)

new_ad_data_2 = {'cost': 900, 'description': 'Отличный гараж', 'address': '12 микрорайон', 'action': 'Продажа'}
garage_data = Garage.objects.create(total_square=20, number_of_floors=3)
new_ad_2 = Ad.objects.create(region=new_city_2, user=dan, content_object=garage_data, **new_ad_data)


all_ads = Ad.objects.all()
current_ad = Ad.filter(region__name='Саяногорск', action='Продажа', user__username='dan', content_type=ContentType.objects.get_for_model(Garage))
current_ad_data = current_ad[0].content_object