"""
Test table endpoint module.
"""

import rest_framework

from . import test_base


class TableEndpointTests(test_base.TestBase):
    """
    Table endpoint test.
    """

    def test_create_table(self):
        """
        Test creating a dynamic model.

        Tests POST and GET methods of the /table endpoint.
        """
        data = {
            "test_field_1": "string",
            "test_field_2": "boolean",
            "some_other_field": "number",
        }
        expected_response = {
            "test_field_1": "text",
            "test_field_2": "boolean",
            "some_other_field": "integer",
        }

        response = self.client.post("/table", data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        response = self.client.get("/table/1")

        self.assertEqual(response.json(), expected_response)

    def test_update_table(self):
        """
        Test updating a dynamic model.

        Tests PUT method of the /table endpoint.
        """
        data = {
            "a_field": "string",
            "b_field": "string",
            "c_field": "number",
            "d_field": "boolean",
        }
        expected_response = {
            "a_field": "text",
            "b_field": "text",
            "c_field": "integer",
            "d_field": "boolean",
        }

        response = self.client.post("/table", data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        update_data = {
            "a_field": "number",
            "b_field": "string",
            "c_field": "boolean",
            "d_field": "string",
        }
        expected_response = {
            "a_field": "integer",
            "b_field": "text",
            "c_field": "boolean",
            "d_field": "text",
        }

        response = self.client.put("/table/1", update_data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)

        response = self.client.get("/table/1")

        self.assertEqual(response.json(), expected_response)
