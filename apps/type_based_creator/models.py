import django

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
    data: dict[str, int | float | bool | str], id: int
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
                "managed": True,
            },
        ),
        "id": django.db.models.OneToOneField(
            ID, on_delete=django.db.models.CASCADE, primary_key=True
        ),
        "__module__": "type_based_creator.models",
    }

    for title, value in data.items():
        attrs[title] = TYPE_TO_FIELD_MAP[type(value)]()

    return type(f"Table{id}", (django.db.models.Model,), attrs)
