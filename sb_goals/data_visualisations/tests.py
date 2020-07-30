# pages/tests.py
from django.test import TestCase


class DataVisualisationsTests(TestCase):
    def test_data_vis_index_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

