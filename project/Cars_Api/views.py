from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import CarModel
from .serializers import CarSerializer, CarsGet, CarsPop, CarsUpdate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Avg, Count, Min
from django.http import Http404
import requests

# Create your views here.

# Download the list of Dealers
makes_url = r'https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=csv'
makes = requests.get(makes_url).text
makes = [i.split(',') for i in makes.split('\r')][1:-1]
makes = ([i[1].lower() for i in makes])


class Cars(APIView):
    def post(self, request):
        make = request.data['make'].lower()
        if make not in makes:
            return Response({"message": "Make doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        models_url = f'https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make}?format=csv'
        models = requests.get(models_url).text
        models = [i.split(',') for i in models.split('\r')][1:-1]
        models = ([i[3].lower() for i in models])
        model = request.data['model'].lower()
        if model not in models:
            return Response({"message": "Model doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(data={"make": make.capitalize(), "model": model.capitalize(), "rate": request.data["rate"]})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        cars = CarModel.objects.values('make', 'model').annotate(id=Min('id'), avg_rating=Avg('rate')).order_by('-avg_rating')
        serializer = CarsGet(cars, many=True)
        if not serializer:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)


class CarsRating(APIView):
    def get_object(self, id):
        try:
            return CarModel.objects.get(id=id)
        except CarModel.DoesNotExist:
            raise Http404("Could not find the car...")

    def post(self, request):
        car = self.get_object(request.data['id'])
        if 1 <= request.data['rating'] <= 5:
            car.rate = request.data['rating']
            car.save()
        else:
            return Response({"message": "Value does not satisfy the range [1,5]"}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
        return Response(status=status.HTTP_201_CREATED)


class DeleteCar(APIView):
    def get_object(self, id):
        try:
            return CarModel.objects.get(id=id)
        except CarModel.DoesNotExist:
            raise Http404("Could not find the car...")

    def delete(self, request, id):
        car = self.get_object(id)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PopularCars(APIView):
    def get(self, request):
        cars = CarModel.objects.values('make', 'model').annotate(id=Min('id'), rates_number=Count('rate')).order_by('-rates_number')
        serializer = CarsPop(cars, many=True)
        return Response(serializer.data)
