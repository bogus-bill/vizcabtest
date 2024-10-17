from django.urls import path
from .views import building_surface, building_usage, building_carbon_footprint

urlpatterns = [
    path('buildings/<int:building_id>/surface/', building_surface, name='building_surface'),
    path('buildings/<int:building_id>/usage/', building_usage, name='building_usage'),
    path('buildings/<int:building_id>/carbon-footprint/', building_carbon_footprint, name='building_carbon_footprint'),
]
