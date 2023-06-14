"""
Serializers module.
"""
import logging
import typing

import rest_framework.serializers

from . import errors

logger = logging.getLogger(__name__)

# pylint: disable=abstract-method


class AnyFieldSerializer(rest_framework.serializers.Serializer):
    """
    Any field serializer.

    Serializer which accepts any JSON and validates that values are of the expected type.
    """

    def to_internal_value(
        self, data: dict[typing.Any, typing.Any]
    ) -> dict[str, int | float | bool | str]:
        """
        Validate the data.
        """
        for key, value in data.items():
            if key == "id":
                raise errors.BadRequest
            if not isinstance(value, (int, float, str, bool)):
                raise errors.BadRequest

        return data

    def to_representation(self, instance: typing.Any) -> typing.Any:
        """
        Convert the instance to its representation.
        """
        return instance


class TitleToTypeSerializer(rest_framework.serializers.Serializer):
    """
    Title to type Serializer.

    Serializer which expect JSON data in the format:
    {
        "title": "type"
    }

    Allowed types are: number, string, boolean.
    """

    def to_internal_value(
        self, data: dict[typing.Any, typing.Any]
    ) -> dict[str, int | float | bool | str]:
        """
        Validate the data.
        """
        for key, value in data.items():
            if key == "id":
                raise errors.BadRequest

            if value not in {"number", "string", "boolean"}:
                raise errors.BadRequest

            # some stupid magic because it's 1am and I'm tired
            if value == "number":
                data[
                    key
                ] = 1  # can't cast boolean to double precision so keeping it as int

            elif value == "boolean":
                data[key] = True

        return data

    def to_representation(self, instance: typing.Any) -> typing.Any:
        """
        Convert the instance to its representation.
        """
        return instance


class RowResponseSerializer(rest_framework.serializers.Serializer):
    """
    Row response serializer.

    Serializer for reponse to the dynamic models row GET request.
    """

    def to_representation(self, instance: typing.Any) -> dict[str, typing.Any]:
        model_dict = {}

        for attr, value in instance.__dict__.items():
            if not attr.startswith("_") and attr != "id":
                model_dict[attr] = str(value)

        return model_dict
