from django.shortcuts import render


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .data_loader import load_data
from .utils import get_building_surface, get_building_usage, get_building_carbon_footprint


# Load the building data
batiments_data = load_data('batiments.json')


@api_view(['GET'])
def building_surface(request, building_id):
    """
    API endpoint to calculate the total surface area of a building.
    """
    surface = get_building_surface(building_id)
    return Response({'building_id': building_id, 'total_surface': surface})


@api_view(['GET'])
def building_usage(request, building_id):
    """
    API endpoint to get the primary usage of a building.
    """
    usage = get_building_usage(building_id)
    return Response({'building_id': building_id, 'primary_usage': usage})


@api_view(['GET'])
def building_carbon_footprint(request, building_id):
    """
    API endpoint to calculate the carbon footprint of a building.
    """
    carbon_footprint = get_building_carbon_footprint(building_id)
    return Response({'building_id': building_id, 'carbon_footprint': carbon_footprint})
