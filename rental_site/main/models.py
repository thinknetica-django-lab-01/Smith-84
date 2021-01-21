from django.db import models

# Create your models here.


class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rubrics(models.Model):
    ACTION_CHOICES = [
        ('Продажа', 'Продажа'),
        ('Аренда', 'Аренда')
    ]
    category = models.CharField(max_length=10, choices=ACTION_CHOICES, default='Sell')

    def __str__(self):
        return self.category


class ApartmentAd(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField()
    number_rooms = models.PositiveSmallIntegerField()
    total_square = models.PositiveSmallIntegerField()
    kitchen_square = models.PositiveSmallIntegerField()
    living_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    ad_description = models.CharField(max_length=255, default='')
    ad_address = models.CharField(max_length=200, default='')
    category = models.ForeignKey(Rubrics, on_delete=models.CASCADE)


class RoomAd(models.Model):
    floor = models.PositiveSmallIntegerField()
    living_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    ad_description = models.CharField(max_length=255, default='')
    ad_address = models.CharField(max_length=200, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    category = models.ForeignKey(Rubrics, on_delete=models.CASCADE)


class GarageAd(models.Model):
    floor = models.PositiveSmallIntegerField()
    total_square = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    ad_description = models.CharField(max_length=255, default='')
    ad_address = models.CharField(max_length=200, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    category = models.ForeignKey(Rubrics, on_delete=models.CASCADE)


class LandPlotAd(models.Model):
    total_square = models.PositiveIntegerField()
    cost = models.PositiveIntegerField()
    ad_description = models.CharField(max_length=255, default='')
    ad_address = models.CharField(max_length=200, default='')
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    category = models.ForeignKey(Rubrics, on_delete=models.CASCADE)


