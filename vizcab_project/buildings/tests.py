from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch
from buildings.data_loader import load_data


class BuildingAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.building_id = 1  # Use the ID of an existing building in your data
    
    @patch('buildings.data_loader.load_data')
    def test_get_building_surface(self, mock_load_data):
        # Mock data
        mock_batiments = [
            {
                "id": 1,
                "nom": "Building 1",
                "surface": 500.0,
                "zoneIds": [1, 2],
                "usage": 1,
                "periodeDeReference": 50
            }
        ]
        mock_zones = [
            {"id": 1, "nom": "Zone 1", "surface": 200.0, "usage": 1, "constructionElements": []},
            {"id": 2, "nom": "Zone 2", "surface": 300.0, "usage": 1, "constructionElements": []},
        ]

        # Mock the load_data function to return this data
        mock_load_data.side_effect = lambda filename: mock_batiments if filename == 'batiments.json' else mock_zones

        # Perform GET request to surface API
        response = self.client.get(reverse('building_surface', kwargs={'building_id': self.building_id}))

        # Assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the returned surface is correct
        expected_surface = 500.0
        self.assertEqual(response.data['total_surface'], expected_surface)
    
    @patch('buildings.data_loader.load_data')
    def test_get_building_usage(self, mock_load_data):
        # Mock data
        mock_batiments = [
            {
                "id": 1,
                "nom": "Building 1",
                "surface": 500.0,
                "zoneIds": [1, 2],
                "usage": 1,
                "periodeDeReference": 50
            }
        ]
        mock_zones = [
            {"id": 1, "nom": "Zone 1", "surface": 200.0, "usage": 1, "constructionElements": []},
            {"id": 2, "nom": "Zone 2", "surface": 300.0, "usage": 2, "constructionElements": []},
        ]
        mock_usages = [
            {"id": 1, "label": "Residential"},
            {"id": 2, "label": "Commercial"}
        ]

        # Mock the load_data function to return this data
        mock_load_data.side_effect = lambda filename: {
            'batiments.json': mock_batiments,
            'zones.json': mock_zones,
            'usages.json': mock_usages
        }[filename]

        # Perform GET request to usage API
        response = self.client.get(reverse('building_usage', kwargs={'building_id': self.building_id}))

        # Assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the returned primary usage is correct (Commercial)
        expected_usage = "Commercial"
        self.assertEqual(response.data['primary_usage'], expected_usage)

    @patch('buildings.data_loader.load_data')
    def test_get_building_carbon_footprint(self, mock_load_data):
        # Mock data
        mock_batiments = [
            {
                "id": 1,
                "nom": "Building 1",
                "surface": 500.0,
                "zoneIds": [1],
                "usage": 1,
                "periodeDeReference": 50
            }
        ]
        mock_zones = [
            {"id": 1, "nom": "Zone 1", "surface": 200.0, "usage": 1, "constructionElements": [{"id": 1, "quantite": 100}]},
        ]
        mock_construction_elements = [
            {"id": 1, "nom": "Concrete", "unite": "m3", "impactUnitaireRechauffementClimatique": {
                "production": 2.5, "construction": 1.0, "exploitation": 0.5, "finDeVie": 0.2
            }}
        ]

        # Mock the load_data function to return this data
        mock_load_data.side_effect = lambda filename: {
            'batiments.json': mock_batiments,
            'zones.json': mock_zones,
            'construction_elements.json': mock_construction_elements
        }[filename]

        # Perform GET request to carbon footprint API
        response = self.client.get(reverse('building_carbon_footprint', kwargs={'building_id': self.building_id}))

        # Assert the response is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the returned carbon footprint is correct
        expected_footprint = (2.5 + 1.0 + 0.5 + 0.2) * 100  # 420.0
        self.assertEqual(response.data['carbon_footprint'], expected_footprint)
