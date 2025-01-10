import math
from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.test import TestCase

from rest_framework import status

from common.constant import constant
from common.serializers import BaseResponseSerializer
from kami_airlines.services import AirplaneService


class AirplaneServiceTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "data": [
                {"id": 1, "passenger_assumptions": 50},
                {"id": 2, "passenger_assumptions": 100},
            ]
        }
        self.invalid_data = {"data": [{"id": 1}]}

    def test_service_process_with_valid_data(self):
        """
        Test the service processes valid data and returns expected results.
        """
        response = AirplaneService.execute({"data": self.valid_data["data"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("airplanes", response.data["data"])

        # Verify specific calculation for the first airplane
        airplane = response.data["data"]["airplanes"][0]
        expected_fuel_consumption = math.log(1) * 0.80 + (50 * 0.002)
        self.assertAlmostEqual(
            airplane["fuel_consumption_per_minute"], expected_fuel_consumption, places=2
        )

    def test_service_process_with_missing_fields(self):
        """
        Test the service handles missing fields in the input data gracefully.
        """
        response = AirplaneService.execute({"data": self.invalid_data["data"]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            [constant["ErrorAirplaneRequestData"]], response.data["errors"]
        )

    def test_service_process_with_zero_consumption(self):
        """
        Test the service handles cases where fuel consumption is zero.
        """
        zero_consumption_data = {"data": [{"id": 1, "passenger_assumptions": 0}]}
        response = AirplaneService.execute({"data": zero_consumption_data["data"]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            [constant["ErrorFuelConsumptionZero"]], response.data["errors"]
        )

    def test_service_process_with_invalid_airplane_id(self):
        """
        Test the service handles invalid airplane IDs (e.g., negative values).
        """
        invalid_id_data = {"data": [{"id": -1, "passenger_assumptions": 50}]}
        response = AirplaneService.execute({"data": invalid_id_data["data"]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual([constant["ErrorAirplaneId"]], response.data["errors"])

    @patch(
        "kami_airlines.services.AirplaneService.execute",
        MagicMock(
            return_value=BaseResponseSerializer.error_response(
                constant["SomethingWentWrong"],
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while processing the airplane data.",
            )
        ),
    )
    def test_service_process_with_exception(self):
        """
        Test the service with unexpected error raise.
        """
        response = AirplaneService.execute(
            {"data": [{"id": 1, "passenger_assumptions": 50}]}
        )
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertIn(
            "An error occurred while processing the airplane data.",
            response.data["message"],
        )
