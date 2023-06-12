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
        logger.warning(f"data is: {data}")

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
