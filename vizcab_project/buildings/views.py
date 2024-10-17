from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .logic import compute_building_surface, compute_building_usage, compute_building_carbon_footprint


@api_view(['GET'])
def building_surface(request, building_id):
    """
    API endpoint to calculate the total surface area of a building.
    """
    surface = compute_building_surface(building_id)
    if surface is None:
        return Response({'detail': 'Building not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'building_id': building_id, 'total_surface': surface})


@api_view(['GET'])
def building_usage(request, building_id):
    """
    API endpoint to get the primary usage of a building.
    """
    usage = compute_building_usage(building_id)
    if usage is None:
        return Response({'detail': 'Building not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'usage_label': usage})


@api_view(['GET'])
def building_carbon_footprint(request, building_id):
    """
    API endpoint to calculate the carbon footprint of a building.
    """
    carbon_footprint = compute_building_carbon_footprint(building_id)
    if carbon_footprint is None:
        return Response({'detail': 'Building not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'carbon_id': building_id, 'carbon_footprint': carbon_footprint})
