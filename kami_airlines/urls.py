from django.urls import path

from kami_airlines.views import AirplaneViewSet

urlpatterns = [
    path(
        "airplanesFuelConsumptionCreate/",
        AirplaneViewSet.as_view({"post": "create"}),
        name="create_airplane_fuel_consumption",
    ),
]
