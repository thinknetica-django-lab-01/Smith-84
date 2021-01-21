from django.db import models

# Create your models here.

# товар, категория, тэги, продавец


class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Apartment(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField()
    number_rooms = models.PositiveSmallIntegerField()
    total_square = models.PositiveSmallIntegerField()
    kitchen_square = models.PositiveSmallIntegerField()
    living_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=200, default='')
    ACTION_CHOICES = [
        ('Продажа', 'Продажа'),
        ('Аренда', 'Аренда'),
        ('Посуточно', 'Посуточно')
    ]
    action = models.CharField(choices=ACTION_CHOICES)


class Room(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField()
    living_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=200, default='')
    ACTION_CHOICES = [
        ('Продажа', 'Продажа'),
        ('Аренда', 'Аренда'),
        ('Посуточно', 'Посуточно')
    ]
    action = models.CharField(choices=ACTION_CHOICES)


class Garage(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField()
    total_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=200, default='')
    ACTION_CHOICES = [
        ('Продажа', 'Продажа'),
        ('Аренда', 'Аренда')
    ]
    action = models.CharField(choices=ACTION_CHOICES)


class LandPlot(models.Model):
    total_square = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    description = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=200, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

