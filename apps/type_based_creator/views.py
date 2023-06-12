import django

import rest_framework.generics
import rest_framework.response

from . import serializers
from . import models


class TableView(rest_framework.generics.GenericAPIView):
    """API view for the current authenticated user."""

    queryset = models.ID.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_instance = models.ID.objects.create()

            GeneratedModel = models.dynamic_model_generator(
                serializer.validated_data, id_instance.pk
            )

            # Save the model to the database
            with django.db.connection.schema_editor() as schema_editor:
                schema_editor.create_model(GeneratedModel)

            table_instance = GeneratedModel.objects.create(
                id=id_instance, **request.data
            )
            table_instance.save()

            return rest_framework.response.Response(
                {"message": f"Created new dynamic model with ID {id_instance.pk}."},
                status=200,
            )

    def get_serializer_class(self):
        return serializers.AnyFieldSerializer
