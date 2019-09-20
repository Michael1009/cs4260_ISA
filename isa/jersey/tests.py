from django.test import TestCase
from django.test import Client


class JerseyTest(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        # creating instance of a client.
        self.client = Client()
        logged_in = self.client.login(username='www', password='$3cureUS')

    def test_createJersey(self):
        # Issue a GET request.
        response = self.client.post(
            '/jersey/api/Jersey/create',
            {
                'team': 'ExampleTeam',
                'number': '1',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
            })

        self.assertEqual(response.status_code, 201)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
# Create your tests here.
