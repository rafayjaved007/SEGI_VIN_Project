from django.db import models


# Create your models here.
class Vehicle(models.Model):
    vin = models.CharField(max_length=17)

    year = models.IntegerField()
    model = models.CharField(max_length=100, null=True)
    make = models.CharField(max_length=100)
    engine = models.CharField(max_length=100, null=True)


class BAPMapping(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    part = models.CharField(max_length=50)
    engine = models.CharField(max_length=150, null=True)
    part_number = models.TextField()
    link = models.CharField(max_length=500)
    inventory = models.IntegerField(default=0)
    source = models.CharField(max_length=100, default='BuyAutoParts')
    image_url = models.CharField(max_length=500, null=True)


class ValeoMapping(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    # part = models.CharField(max_length=50)
    engine = models.IntegerField()
    # engine = models.CharField(max_length=50, null=True)s
    # part_number = models.CharField(max_length=150)
    link = models.CharField(max_length=100)
    inventory = models.IntegerField(default=0)
    source = models.CharField(max_length=100, default='Valeo')
    image_url = models.CharField(max_length=100, null=True)
    engine_fuel = models.CharField(max_length=50)
    ref_new = models.CharField(max_length=50, null=True)
    ref_reman = models.CharField(max_length=50, null=True)
    ref_wo_clutch = models.CharField(max_length=50, null=True)
    clutch_assembly = models.CharField(max_length=50, null=True)


class DensoMapping(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    part_number = models.CharField(max_length=150)
    image_url = models.CharField(max_length=100, null=True)


class SandenMapping(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    engine = models.CharField(max_length=50)
    part_number = models.CharField(max_length=150)
    image_url = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
