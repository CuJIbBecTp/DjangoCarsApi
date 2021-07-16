from django.db import models

# Create your models here.


class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    rate = models.FloatField(max_length=32)

    def __str__(self):
        return f"Car(make = {self.make}, model = {self.model}, rate = {self.rate})"