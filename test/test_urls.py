from django.urls import resolve, reverse

from rest_framework.test import APITestCase


class AirplaneURLTests(APITestCase):
    def test_airplane_url_resolves_to_correct_view(self):
        """
        Test if the airplane URL resolves to the correct view.
        """
        url = reverse("create_airplane_fuel_consumption")
        resolved_view = resolve(url).func.__name__
        self.assertEqual(resolved_view, "AirplaneViewSet")
