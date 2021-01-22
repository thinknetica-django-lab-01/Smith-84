from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

# товар, категория, тэги, продавец


class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенный пункты'



class Ad(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=200, default='')
    ACTION_CHOICES = [
        ('Продажа', 'Продажа'),
        ('Аренда', 'Аренда'),
        ('Посуточно', 'Посуточно')
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

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Apartment(models.Model):
    floor = models.PositiveSmallIntegerField()
    number_of_rooms = models.PositiveSmallIntegerField()
    total_square = models.PositiveSmallIntegerField()
    kitchen_square = models.PositiveSmallIntegerField()
    living_square = models.PositiveSmallIntegerField()


class Room(models.Model):
    floor = models.PositiveSmallIntegerField()
    living_square = models.FloatField()


class Garage(models.Model):
    number_of_floors = models.PositiveSmallIntegerField()
    total_square = models.FloatField()


class LandPlot(models.Model):
    total_square = models.FloatField()

