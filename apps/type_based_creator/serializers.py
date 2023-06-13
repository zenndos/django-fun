import logging
import typing
import rest_framework.serializers

from . import errors

logger = logging.getLogger(__name__)


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
        for k, v in data.items():
            if k == "id":
                raise errors.BadRequest
            if not isinstance(v, (int, float, str, bool)):
                raise errors.BadRequest

        return data

    def to_representation(self, instance):
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
        for k, v in data.items():
            if k == "id":
                raise errors.BadRequest

            if v not in {"number", "string", "boolean"}:
                raise errors.BadRequest

            # some stupid magic because it's 1am and I'm tired
            elif v == "number":
                data[
                    k
                ] = 1  # can't cast boolean to double precision so keeping it as int

            elif v == "boolean":
                data[k] = True

        return data

    def to_representation(self, instance):
        """
        Convert the instance to its representation.
        """
        return instance


class DynamicModelSerializer(rest_framework.serializers.Serializer):
    def to_representation(self, instance):
        model_dict = {}

        for attr, value in instance.__dict__.items():
            if not attr.startswith("_") and attr != "id_id":
                model_dict[attr] = str(value)

        return model_dict
