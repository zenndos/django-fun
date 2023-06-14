"""
Test row endoint module.
"""

import rest_framework

from . import test_base


class RowEndpointTests(test_base.TestBase):
    """
    Row and rows endpoints test.
    """

    def test_create_table(self):
        """
        Test creating a row of dynamic model.

        Tests POST and GET methods of the /row and /rows endpoints.
        """
        data = {
            "test_field_1": "string",
            "test_field_2": "boolean",
            "some_other_field": "number",
        }

        response = self.client.post("/table", data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        row_1_data = {
            "test_field_1": "abc",
            "test_field_2": True,
            "some_other_field": 42,
        }
        row_2_data = {
            "test_field_1": "def",
            "test_field_2": False,
            "some_other_field": 27,
        }

        expetected_response = [
            {
                "test_field_1": "abc",
                "test_field_2": "True",
                "some_other_field": "42",
            },
            {
                "test_field_1": "def",
                "test_field_2": "False",
                "some_other_field": "27",
            },
        ]

        response = self.client.post("/table/1/row", row_1_data, format="json")
        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        response = self.client.post("/table/1/row", row_2_data, format="json")
        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        response = self.client.get("/table/1/rows")
        print(response.json())
        self.assertEqual(response.json(), expetected_response)
