import django

import rest_framework.generics
import rest_framework.response

from . import serializers
from . import models
from . import errors

import logging

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

    def get(self, request, *args, **kwargs) -> django.db.models.Model:
        id_value = kwargs["id"]

        query_dict = _build_get_query_dict(id_value)
        generated_model = models.dynamic_model_generator(
            query_dict, id_value, to_insert=False
        )
        django.apps.apps.register_model("type_based_creator", generated_model)

        table_columns = models.query_columns(generated_model)
        table_columns.pop("id")

        return rest_framework.response.Response(table_columns, status=200)

    def post(self, request):
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

    def put(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_value = kwargs["id"]

            query_dict = _build_get_query_dict(id_value)
            generated_model = models.dynamic_model_generator(query_dict, id_value)

            models.update_dynamic_model(request.data, generated_model, id_value)

            return rest_framework.response.Response(
                {"message": f"Updated dynamic model with ID {id_value}."},
                status=200,
            )

    def get_serializer_class(self):
        if "cool-table" in self.request.path:
            return serializers.AnyFieldSerializer
        return serializers.TitleToTypeSerializer


class RowView(rest_framework.generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs) -> django.db.models.Model:
        id_value = kwargs["id"]

        query_dict = _build_get_query_dict(id_value)
        generated_model = models.dynamic_model_generator(query_dict, id_value)
        django.apps.apps.register_model("type_based_creator", generated_model)

        instances = generated_model.objects.all()
        response_data = []
        for instance in instances:
            serializer = serializers.DynamicModelSerializer(instance)
            response_data.append(serializer.data)

        return rest_framework.response.Response(response_data, status=200)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_value = kwargs["id"]

            query_dict = _build_get_query_dict(id_value)
            generated_model = models.dynamic_model_generator(query_dict, id_value)

            django.apps.apps.register_model("type_based_creator", generated_model)

            table_instance = generated_model(**request.data)
            table_instance.save()

            return rest_framework.response.Response(
                {"message": f"Created new dynamic model with ID {table_instance}."},
                status=200,
            )

    def get_serializer_class(self):
        return serializers.AnyFieldSerializer


def _build_get_query_dict(id_value):
    empty_model = models.dynamic_model_generator({}, id_value)
    cols = models.query_columns(empty_model)
    query_dict = {}
    for k, v in cols.items():
        if k == "id_id":
            ...
        else:
            query_dict[k] = POSTGRES_TYPE_TO_FIELD_MAP[v]
    return query_dict
