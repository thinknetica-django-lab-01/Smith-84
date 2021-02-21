import uuid
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from pytils.translit import slugify
from django.contrib.sites.models import Site

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user)


class Region(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True, db_index=True)
    slug = models.SlugField(primary_key=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'


class Ad(models.Model):
    uniq_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    date_added = models.DateField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    ACTION_CHOICES = [
        ('sell', 'Продажа'),
        ('rent', 'Аренда'),
    ]
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={
        'model__in': (
            'apartment',
            'room',
            'garage',
            'landplot'
        )
    })
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.description)[:30].replace(' ', '-')}-{str(self.uniq_id)}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ad_detail', kwargs={'slug': self.slug})

    def get_full_absolute_url(self):
        domain = Site.objects.get_current().domain
        return f'http://{domain}{self.get_absolute_url()}'

    def __str__(self):
        return self.description[:40]

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['date_added']


class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, default=True)
    image = models.ImageField(upload_to='image_folder', verbose_name='Изображение')


class Realty(models.Model):
    total_square = models.FloatField(default=True)

    class Meta:
        abstract = True


class Apartment(Realty):
    BUILDING_CHOICES = ([
        ('new', 'Новостройка'),
        ('second', 'Вторичка')
    ])
    floor = models.PositiveSmallIntegerField()
    number_of_rooms = models.PositiveSmallIntegerField()
    kitchen_square = models.FloatField()
    living_square = models.FloatField()
    building = models.CharField(max_length=20, choices=BUILDING_CHOICES)

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'

    def __str__(self):
        return 'Квартира'


class Room(Realty):
    floor = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

    def __str__(self):
        return 'Комната'


class Garage(Realty):
    number_of_floors = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Гараж'
        verbose_name_plural = 'Гаражы'

    def __str__(self):
        return 'Гараж'


class LandPlot(Realty):
    class Meta:
        verbose_name = 'Земельный участок'
        verbose_name_plural = 'Земельные участки'

    def __str__(self):
        return 'Земля'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    ads = models.ManyToManyField(Ad)

    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.name).replace(' ', '-')}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Subscribers(models.Model):
    email = models.EmailField(unique=True)
