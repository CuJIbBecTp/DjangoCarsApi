from django.urls import path
from .views import Cars, CarsRating, DeleteCar, PopularCars

urlpatterns = [
    path('cars/', Cars.as_view()),
    path('rate/', CarsRating.as_view()),
    path('cars/<int:id>/', DeleteCar.as_view()),
    path('popular/', PopularCars.as_view()),
]
