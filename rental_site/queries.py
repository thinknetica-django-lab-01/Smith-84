# После того как модели описаны и созданы, теперь необходимо с их помощью уметь создавать и получать данные.
#
# Изучить методы create(), save(), filter(), all(), get()
#
# Запустить код из django shell
from .main.models import *
from django.contrib.auth.models import User
# Задачи
# Создать несколько товаров методом save() и create() и
# потом получить их отфильтровав по разным категориям, используя filter().

new_city_1 = Region(name='Абакан')
new_city_1.save()
new_city_2 = Region(name='Саяногорск')
new_city_2.save()
john = User.objects.create_user('john', 'john@gmail.com', '123123123j')
dan = User.objects.create_user('dan', 'john@gmail.com', '123123123j')
john_profile = Profile.objects.create(user=john, phone_number='+79095696363')
dan_profile = Profile.objects.create(user=dan, phone_number='+79095696362')