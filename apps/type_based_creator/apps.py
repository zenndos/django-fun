import django
import logging

import logging

logger = logging.getLogger(__name__)


class MyAppConfig(django.apps.AppConfig):
    name = "type_based_creator"

    def ready(self):
        from . import models

        if (
            not models.ID._meta.db_table
            in django.db.connection.introspection.table_names()
        ):
            with django.db.connection.schema_editor() as schema_editor:
                schema_editor.create_model(models.ID)
                logger.info("ID table created")
        else:
            logger.info("ID table already exists")

        from django.core.management import call_command

        call_command("makemigrations")
        call_command("migrate")
