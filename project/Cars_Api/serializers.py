from rest_framework import serializers
from .models import CarModel


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    make = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    rate = serializers.FloatField()

    def create(self, validated_data):
        return CarModel.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.make = validated_data.get('make', instance.make)
        instance.model = validated_data.get('model', instance.model)
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance
