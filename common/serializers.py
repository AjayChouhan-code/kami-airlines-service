from rest_framework import serializers
from rest_framework.response import Response

from common.constant import constant


class ErrorListField(serializers.ListField):
    error = serializers.DictField(required=False)


class BaseResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    count = serializers.IntegerField(required=False)
    errors = ErrorListField(required=False)
    data = serializers.JSONField(required=False)
    message = serializers.CharField()
    code = serializers.IntegerField()

    @staticmethod
    def pagination_success_response(result, count, status):
        return Response(
            BaseResponseSerializer(
                {
                    "success": True,
                    "count": count,
                    "data": (
                        result.data
                        if isinstance(result, serializers.ModelSerializer)
                        else result
                    ),
                    "code": status,
                    "message": constant["SuccessfullyCompleted"],
                }
            ).data,
            status=status,
        )

    @staticmethod
    def success_response(result, status):
        return Response(
            BaseResponseSerializer(
                {
                    "success": True,
                    "data": (
                        result.data
                        if isinstance(result, serializers.ModelSerializer)
                        else result
                    ),
                    "code": status,
                    "message": (
                        constant["SuccessfullyCreated"]
                        if status == 201
                        else constant["SuccessfullyCompleted"]
                    ),
                }
            ).data,
            status=status,
        )

    @staticmethod
    def success_response_with_dynamic_msg(result, status, message):
        return Response(
            BaseResponseSerializer(
                {
                    "success": True,
                    "data": (
                        result.data
                        if isinstance(result, serializers.ModelSerializer)
                        else result
                    ),
                    "code": status,
                    "message": (
                        message if status == 201 else constant["SuccessfullyCompleted"]
                    ),
                }
            ).data,
            status=status,
        )

    @staticmethod
    def error_response(error, status, message):
        if isinstance(error, Exception):
            return Response(
                BaseResponseSerializer(
                    {
                        "success": False,
                        "code": status,
                        "message": message,
                        "errors": [str(error)],
                        "data": {},
                    }
                ).data,
                status=status,
            )
        if isinstance(error, list):
            return Response(
                BaseResponseSerializer(
                    {
                        "success": False,
                        "message": message,
                        "data": {},
                        "code": status,
                        "errors": error,
                    }
                ).data,
                status=status,
            )
        return Response(
            BaseResponseSerializer(
                {
                    "success": False,
                    "message": message,
                    "data": {},
                    "code": status,
                    "errors": [error],
                }
            ).data,
            status=status,
        )


class BadRequestResponseSerializer(serializers.Serializer):
    """
    This serializer class is used to manage the response of bad request in endpoint documentation.
    """

    success = serializers.BooleanField(default=False)
    errors = ErrorListField(required=False)
    data = serializers.JSONField(default={}, required=False)
    message = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)
