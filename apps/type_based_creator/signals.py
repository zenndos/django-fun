import django
import typing

from django.db import connection

from . import models

import logging

logger = logging.getLogger(__name__)


def create_ids_table():
    if not models.ID._meta.db_table in connection.introspection.table_names():
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(models.ID)
            logger.info("ID table created")
    else:
        logger.warning("ID table already exists")
