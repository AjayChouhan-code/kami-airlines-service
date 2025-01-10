import logging
from http import HTTPStatus

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from common.constant import constant
from common.custom_auto_schema import CustomCodeAutoSchema
from common.serializers import BadRequestResponseSerializer, BaseResponseSerializer
from kami_airlines.serializers import (
    AirplaneRequestDataSerializer,
    AirplaneResponseDataSerializer,
)
from kami_airlines.services import AirplaneService

logger = logging.getLogger("kami_logger")


class AirplaneViewSet(viewsets.ViewSet):
    """
    This class inherits the base class ``ViewSet`` and it includes the methods ``create`` to create airplanes.
    """

    @staticmethod
    @swagger_auto_schema(
        auto_schema=CustomCodeAutoSchema,
        responses={
            "201": AirplaneResponseDataSerializer(),
            "400": BadRequestResponseSerializer,
        },
        operation_id="Create airplane data",
        operation_description="This method is used to create airplane data and calculate fuel consumption and max flight time.",
    )
    def create(request):
        """
        This method is used to create airplane data and calculate fuel consumption and max flight time.
        :param request: Request object.
        :type request: request
        :return: Response containing airplane data, fuel consumption and max flight time.
        :rtype: dict
        """
        serial_data = AirplaneRequestDataSerializer(data=request.data)
        if serial_data.is_valid():
            return AirplaneService.execute({"data": serial_data.validated_data["data"]})

        logger.error(
            f"{constant['ErrorLogger'].format('creating airplane data')}: [{status.HTTP_400_BAD_REQUEST}] [{serial_data.errors}]"
        )
        return BaseResponseSerializer.error_response(
            serial_data.errors,
            HTTPStatus.BAD_REQUEST,
            message="Invalid input data provided.",
        )
