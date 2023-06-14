"""
Test base module.
"""

import django
import rest_framework.test


class TestBase(rest_framework.test.APITestCase):
    """
    Test base.

    Base class for test.
    """

    def setUp(self):
        """
        Test setup.

        Rest framework test does not execute ready signal and does not drop
        all tables from the DB, so I have to do it myself.
        """
        with django.db.connection.cursor() as cursor:
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            tables = cursor.fetchall()
            if ("type_based_creator_id",) in tables:
                cursor.execute("DROP TABLE type_based_creator_id")
                cursor.execute(
                    """
                    CREATE TABLE type_based_creator_id (
                        id serial PRIMARY KEY
                    );
                """
                )
