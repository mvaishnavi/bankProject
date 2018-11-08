from django.db import models



class Banks(models.Model):
    name = models.CharField(max_length=50)
    id = models.BigIntegerField(unique=True, primary_key=True)


class Branches(models.Model):
    ifsc = models.CharField(max_length=12, primary_key=True)
    bank = models.ForeignKey(Banks, to_field='id', on_delete=models.CASCADE)
    branch = models.CharField(max_length=75)
    address = models.CharField(max_length=196)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=27)
