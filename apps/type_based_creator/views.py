"""
Views module.
"""
import typing
import logging

import django
import rest_framework.generics
import rest_framework.response

from . import errors, models, serializers

logger = logging.getLogger(__name__)

POSTGRES_TYPE_TO_FIELD_MAP = {
    "boolean": True,
    "double precision": 1.0,
    "integer": 1,
    "bigint": 1,
    "text": "text",
}


class TableView(rest_framework.generics.RetrieveAPIView):
    """API view for the current authenticated user."""

    def get(
        self, request: rest_framework.request.Request, *args, **kwargs
    ) -> rest_framework.response.Response:
        """
        GET method handler.

        :param: request - request object.

        :return: response object.
        """
        id_value = kwargs["id"]

        model_fields = build_model_fields(id_value)
        generated_model = models.dynamic_model_generator(
            model_fields, id_value, to_insert=False
        )
        django.apps.apps.register_model("type_based_creator", generated_model)

        table_columns = models.query_columns(generated_model)
        table_columns.pop("id")

        return rest_framework.response.Response(table_columns, status=200)

    def post(
        self,
        request: rest_framework.request.Request,
    ) -> rest_framework.response.Response:
        """
        POST method handler.

        :param: request - request object.

        :return: response object.
        """
        # pylint: disable=no-member
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_instance = models.ID.objects.create()

            generated_model = models.dynamic_model_generator(
                serializer.validated_data, id_instance.pk, to_insert=True
            )

            # Save the model to the database
            with django.db.connection.schema_editor() as schema_editor:
                schema_editor.create_model(generated_model)
            id_instance.save()

            django.apps.apps.register_model("type_based_creator", generated_model)

            return rest_framework.response.Response(
                {"message": f"Created new dynamic model with ID {id_instance.pk}."},
                status=200,
            )

        raise errors.BadRequest

    def put(
        self, request: rest_framework.request.Request, **kwargs
    ) -> rest_framework.response.Response:
        """
        PUT method handler.

        :param: request - request object.

        :return: response object.

        :raises: errors.BadRequest when the request is invalid.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_value = kwargs["id"]

            model_fields = build_model_fields(id_value)
            generated_model = models.dynamic_model_generator(model_fields, id_value)

            models.update_dynamic_model(request.data, generated_model)

            return rest_framework.response.Response(
                {"message": f"Updated dynamic model with ID {id_value}."},
                status=200,
            )

        raise errors.BadRequest

    def get_serializer_class(self):
        """
        Get the serializer class.

        Sets serializer class based on the request path.

        :return: serializer class.
        """

        if "cool-table" in self.request.path:
            return serializers.AnyFieldSerializer

        return serializers.TitleToTypeSerializer


class RowView(rest_framework.generics.RetrieveAPIView):
    """
    Row view.

    API view for the row of the dynamic table.
    """

    def get(self, request, *args, **kwargs) -> rest_framework.response.Response:
        """
        GET method handler.

        :param: request - request object.

        :return: response object.
        """
        id_value = kwargs["id"]

        model_fields = build_model_fields(id_value)
        generated_model = models.dynamic_model_generator(model_fields, id_value)
        django.apps.apps.register_model("type_based_creator", generated_model)

        instances = generated_model.objects.all()
        response_data = []
        for instance in instances:
            serializer = serializers.RowResponseSerializer(instance)
            response_data.append(serializer.data)

        return rest_framework.response.Response(response_data, status=200)

    def post(self, request, **kwargs) -> rest_framework.response.Response:
        """
        POST method handler.

        :param: request - request object.

        :return: response object.

        :raises: errors.BadRequest when the request is invalid.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_value = kwargs["id"]

            model_fields = build_model_fields(id_value)
            generated_model = models.dynamic_model_generator(model_fields, id_value)

            django.apps.apps.register_model("type_based_creator", generated_model)

            table_instance = generated_model(**request.data)
            table_instance.save()

            return rest_framework.response.Response(
                {"message": f"Created new dynamic model with ID {table_instance}."},
                status=200,
            )

        raise errors.BadRequest

    def get_serializer_class(self):
        """
        Get the serializer class.

        :return: serializer class.
        """
        return serializers.AnyFieldSerializer


def build_model_fields(id_value: str) -> dict[str, typing.Any]:
    """
    Build model fields.

    Query the database for the model columns and build the model fields.

    :param: id_value - id of the model.

    :return: model fields.
    """
    empty_model = models.dynamic_model_generator({}, id_value)
    cols = models.query_columns(empty_model)

    model_fields = {}
    for key, value in cols.items():
        if key == "id_id":
            ...

        else:
            model_fields[key] = POSTGRES_TYPE_TO_FIELD_MAP[value]

    return model_fields
