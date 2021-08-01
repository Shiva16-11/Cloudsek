from django.db import models


class NumberData(models.Model):
    number_one = models.FloatField()
    number_two = models.FloatField()
    total = models.FloatField(null=True)
