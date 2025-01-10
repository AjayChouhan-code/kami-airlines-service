import json
from http import HTTPStatus
from unittest.mock import MagicMock, Mock, patch

from django.urls import reverse

from requests import Session
from rest_framework import status
from rest_framework.test import APITestCase

from common.serializers import BaseResponseSerializer
from kami_airlines.services import AirplaneService


class AirplaneCreateEndpointTest(APITestCase):
    """
    This class is created to test the endpoint for creating airplane data and calculating fuel consumption and max flight time.
    """

    @patch.object(
        Session,
        "post",
        MagicMock(
            return_value=(
                Mock(
                    status_code=HTTPStatus.CREATED,
                    json=Mock(
                        return_value=BaseResponseSerializer.success_response(
                            {
                                "airplanes": [
                                    {
                                        "id": 1,
                                        "fuel_consumption_per_minute": 0.2,
                                        "max_flight_time": 100.0,
                                    }
                                ]
                            },
                            HTTPStatus.CREATED,
                        ).data
                    ),
                )
            )
        ),
    )
    def test_create_airplane_fuel_consumption_valid(self):
        """
        This test case is created to test the valid input for creating airplane data and calculating fuel consumption.
        """
        url = reverse("create_airplane_fuel_consumption")
        valid_data = {
            "data": [
                {
                    "id": 1,
                    "passenger_assumptions": 50,
                }
            ]
        }

        response = self.client.post(url, data=valid_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["airplanes"][0]["id"] == 1
        assert (
            response.data["data"]["airplanes"][0]["fuel_consumption_per_minute"] == 0.1
        )
        assert response.data["data"]["airplanes"][0]["max_flight_time"] == 2000.0
