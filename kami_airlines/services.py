import logging
import math
from http import HTTPStatus

from service_objects.services import Service

from common.constant import constant
from common.serializers import BaseResponseSerializer
from kami_airlines.models import Airplanes

logger = logging.getLogger("kami_logger")


class AirplaneService(Service):
    """
    This class includes the method ``process`` to calculate fuel consumption and max flight time for airplanes.
    """

    def process(self):
        """
        This method is used to calculate fuel consumption and maximum flight time for airplanes.

        :return: JSON response with airplane data, fuel consumption, and max flight time.
        :rtype: dict
        """
        try:
            airplanes = []
            for airplane_data in self.data.get("data"):
                airplane_id = airplane_data.get("id")
                passenger_assumptions = airplane_data.get("passenger_assumptions")

                if airplane_id is None or passenger_assumptions is None:
                    logger.error(
                        f"{constant['ErrorLogger'].format('calculating airplane data')}: [{HTTPStatus.BAD_REQUEST}] [Missing required fields in airplane data]"
                    )
                    return BaseResponseSerializer.error_response(
                        constant["ErrorAirplaneRequestData"],
                        HTTPStatus.BAD_REQUEST,
                        message="Invalid input data.",
                    )

                try:
                    # Calculate fuel capacity
                    fuel_capacity = 200 * airplane_id

                    # Calculate fuel consumption per minute
                    fuel_consumption_per_minute = math.log(airplane_id) * 0.80

                    # Calculate fuel consumption with passenger_assumptions
                    fuel_consumption_with_passengers = fuel_consumption_per_minute + (
                        passenger_assumptions * 0.002
                    )

                    # Ensure no division by zero
                    if fuel_consumption_with_passengers == 0:
                        logger.error(
                            f"{constant['ErrorLogger'].format('calculating airplane data')}: [{HTTPStatus.BAD_REQUEST}] [Fuel consumption per minute is zero for airplane id: {airplane_id}]"
                        )
                        return BaseResponseSerializer.error_response(
                            constant["ErrorFuelConsumptionZero"],
                            HTTPStatus.BAD_REQUEST,
                            message="Invalid input data.",
                        )

                    # Calculate maximum flight time (in minutes)
                    max_flight_time = fuel_capacity / fuel_consumption_with_passengers

                    airplane_info = {
                        "id": airplane_id,
                        "fuel_consumption_per_minute": round(
                            fuel_consumption_with_passengers, 2
                        ),
                        "max_flight_time": round(max_flight_time, 2),
                    }
                    airplanes.append(airplane_info)

                    Airplanes.objects.create(
                        id=airplane_id, passenger_assumptions=passenger_assumptions
                    )

                except ValueError as err:
                    logger.error(
                        f"{constant['ErrorLogger'].format('calculating airplane data')}: [{HTTPStatus.BAD_REQUEST}] [Invalid ID for airplane: {airplane_id}. Must be greater than zero. Error: {str(err)}]"
                    )
                    return BaseResponseSerializer.error_response(
                        constant["ErrorAirplaneId"],
                        HTTPStatus.BAD_REQUEST,
                        message="Invalid input data.",
                    )

            return BaseResponseSerializer.success_response(
                {"airplanes": airplanes}, HTTPStatus.CREATED
            )

        except Exception as err:
            logger.critical(
                f"{constant['ErrorLogger'].format('calculating airplane data')}: [{HTTPStatus.INTERNAL_SERVER_ERROR}] [{str(err)}]"
            )
            return BaseResponseSerializer.error_response(
                str(err),
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message="An error occurred while processing the airplane data.",
            )
