"""
Django apps module.
"""

import logging

import django

logger = logging.getLogger(__name__)


class AppConfig(django.apps.AppConfig):
    """
    Application config.
    """

    name = "type_based_creator"

    def ready(self):
        """
        Application ready signal.

        Code to be executed when the application is ready.
        """
        # pylint: disable=import-outside-toplevel
        # pylint: disable=protected-access
        # pylint: disable=no-member
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
