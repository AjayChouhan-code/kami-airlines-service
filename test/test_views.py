from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class AirplaneViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse("create_airplane_fuel_consumption")
        self.valid_data = {
            "data": [
                {"id": 1, "passenger_assumptions": 50},
                {"id": 2, "passenger_assumptions": 100},
            ]
        }
        self.invalid_data = {"data": [{"id": 1}]}

    def test_create_airplane_with_valid_data(self):
        """
        Test the create method with valid airplane data.
        """
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("airplanes", response.data.get("data"))
        self.assertEqual(len(response.data["data"]["airplanes"]), 2)

    def test_create_airplane_with_invalid_data(self):
        """
        Test the create method with incomplete airplane data.
        """
        response = self.client.post(self.url, self.invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_create_airplane_with_empty_data(self):
        """
        Test the create method with empty request data.
        """
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
