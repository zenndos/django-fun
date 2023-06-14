"""
Models module.
"""

import logging

import django

logger = logging.getLogger(__name__)

TYPE_TO_FIELD_MAP = {
    bool: django.db.models.BooleanField,
    int: django.db.models.IntegerField,
    float: django.db.models.FloatField,
    str: django.db.models.TextField,  # sacrificing CharField for the map
}


class ID(django.db.models.Model):
    """
    ID model.

    This model is used to generate the foreign key for the dynamic models.
    """

    # pylint: disable=too-few-public-methods

    class Meta:
        """
        Meta class.
        """

        app_label = "type_based_creator"


def dynamic_model_generator(
    data: dict[str, int | float | bool | str], id_value: str, to_insert: bool = False
) -> django.db.models.Model:
    """
    Dynamic model generator.

    Generatos a model based on the data provided.

    :param: data - data to be used to generate the model.
    :param: id - id of the model.
    :param: to_insert - weather the model is to be inserted by schema editor.
    """
    attrs = {
        "Meta": type(
            "Meta",
            (),
            {
                "app_label": "type_based_creator",
            },
        ),
        "__module__": "type_based_creator.models",
    }

    if to_insert:
        attrs["related_id"] = (
            django.db.models.ForeignKey(ID, on_delete=django.db.models.CASCADE),
        )

    for title, value in data.items():
        attrs[title] = TYPE_TO_FIELD_MAP[type(value)]()

    attrs["id"] = django.db.models.AutoField(primary_key=True)

    return type(f"Table{id_value}", (django.db.models.Model,), attrs)


def update_dynamic_model(
    data: dict[str, int | float | bool | str],
    dynamic_model: django.db.models.Model,
) -> None:
    """
    Update dynamic model.

    Updated a model based on the data provided.

    :param: data - data to be update the new model with.
    :param: dynamic_model - dynamic model to be updated.
    """
    # pylint: disable=protected-access
    for title, value in data.items():
        new_field = TYPE_TO_FIELD_MAP[type(value)]()
        new_field.name = title

        if not hasattr(dynamic_model, title):
            dynamic_model.add_to_class(title, type(new_field))

            with django.db.connection.schema_editor() as schema_editor:
                schema_editor.add_field(dynamic_model, new_field)

        else:
            current_field = dynamic_model._meta.get_field(title)

            if not isinstance(current_field, type(new_field)):
                dynamic_model.add_to_class(title, type(new_field))

                new_field.model = dynamic_model
                new_field.attname, new_field.column = current_field.get_attname_column()

                with django.db.connection.schema_editor() as schema_editor:
                    schema_editor.alter_field(
                        dynamic_model,
                        current_field,
                        new_field,
                    )


def query_columns(model: django.db.models.Model) -> dict[str, str]:
    """
    Query columns.

    Query columns of django model from database table.

    :param: model - model to use for query.
    """
    # pylint: disable=protected-access
    table_name = model._meta.db_table

    with django.db.connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}';
        """
        )

        column_types = {row[0]: row[1] for row in cursor.fetchall()}

    return column_types
