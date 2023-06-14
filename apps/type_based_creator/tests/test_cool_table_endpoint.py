"""
Test cool table module.
"""

import rest_framework
import rest_framework.test

from . import test_base

# pylint: disable=duplicate-code


class CoolTableEndpointTests(test_base.TestBase):
    """
    Cool table endpoit tests.
    """

    def test_create_table(self):
        """
        Test creating a cool table.

        Tests POST and GET methods of the /cool-table endpoint.
        """
        data = {
            "test_field_1": "abc",
            "test_field_2": True,
            "some_other_field": 42,
        }
        expected_response = {
            "test_field_1": "text",
            "test_field_2": "boolean",
            "some_other_field": "integer",
        }

        response = self.client.post("/cool-table", data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        response = self.client.get("/cool-table/1")

        self.assertEqual(response.json(), expected_response)

    def test_update_table(self):
        """
        Test updating a dynamic model.

        Tests PUT method of the /cool-table endpoint.
        """
        data = {
            "a_field": "def",
            "b_field": "fgfgd",
            "c_field": 12,
            "d_field": False,
        }
        expected_response = {
            "a_field": "text",
            "b_field": "text",
            "c_field": "integer",
            "d_field": "boolean",
        }

        response = self.client.post("/cool-table", data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)

        update_data = {
            "a_field": 11,
            "b_field": "ewrwe",
            "c_field": True,
            "d_field": "some_text",
        }
        expected_response = {
            "a_field": "integer",
            "b_field": "text",
            "c_field": "boolean",
            "d_field": "text",
        }

        response = self.client.put("/cool-table/1", update_data, format="json")

        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)

        response = self.client.get("/cool-table/1")

        self.assertEqual(response.json(), expected_response)
