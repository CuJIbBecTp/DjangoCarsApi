from rest_framework import serializers
from .models import CarModel


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'make', 'model', 'rate']
