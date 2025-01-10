from rest_framework import serializers


class AirplaneRequestSerializer(serializers.Serializer):
    """
    Serializer to validate the input request data for airplane processing.
    """

    id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "Airplane ID is required.",
            "invalid": "Airplane ID must be a valid integer.",
            "min_value": "Airplane ID must be greater than 0.",
        },
    )
    passenger_assumptions = serializers.IntegerField(
        required=True,
        min_value=0,
        error_messages={
            "required": "Number of passenger_assumptions is required.",
            "invalid": "Number of passenger_assumptions must be a valid integer.",
            "min_value": "Number of passenger_assumptions cannot be negative.",
        },
    )


class AirplaneRequestDataSerializer(serializers.Serializer):
    """
    Serializer to handle the top-level request data containing a list of airplanes.
    """

    data = AirplaneRequestSerializer(many=True, required=True)

    def validate_data(self, value):
        """
        Custom validation to ensure the list is not empty.
        """
        if not value:
            raise serializers.ValidationError("The 'data' list cannot be empty.")
        return value


class AirplaneDataSerializer(serializers.Serializer):
    """
    This serializer class is used to provide response of airlines endpoint in documentation.
    """

    id = serializers.IntegerField()
    fuel_consumption_per_minute = serializers.FloatField()
    max_flight_time = serializers.FloatField()


class AirplaneSerializer(serializers.Serializer):
    """
    This serializer class is used to provide response of airlines endpoint in documentation.
    """

    airplanes = AirplaneDataSerializer(many=True, required=False)


class AirplaneResponseDataSerializer(serializers.Serializer):
    """
    This serializer class is used to provide response of airlines endpoint in documentation.
    """

    success = serializers.BooleanField(default=True)
    message = serializers.CharField(required=False)
    data = AirplaneSerializer(many=True, required=False)
    status = serializers.IntegerField(required=False)
