import django
import logging

from . import errors

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

    This model is used to generate the primary key for the dynamic models.
    """

    class Meta:
        app_label = "type_based_creator"


def dynamic_model_generator(
    data: dict[str, int | float | bool | str], id: int, to_insert: bool = False
) -> django.db.models.Model:
    """
    Dynamic model generator.

    Generatos a model based on the data provided.

    :param: data - data to be used to generate the model.
    :param: id - id of the model.
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

    return type(f"Table{id}", (django.db.models.Model,), attrs)


def update_dynamic_model(
    data: dict[str, int | float | bool | str],
    dynamic_model: django.db.models.Model,
    id_value: str,
) -> None:
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

                logger.info(
                    f"current_field: {type(current_field)}, new_field: {type(new_field)}"
                )

                with django.db.connection.schema_editor() as schema_editor:
                    schema_editor.alter_field(
                        dynamic_model,
                        current_field,
                        new_field,
                    )

        # table_instance = get_dynamic_model_instance(id_value)
        # setattr(table_instance, title, value)

    # table_instance.save()


def get_dynamic_model(id_value):
    model_name = f"Table{id_value}"

    DynamicModel = django.apps.apps.get_model("type_based_creator", model_name)

    return DynamicModel


def query_columns(model):
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
