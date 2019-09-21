from django.test import TestCase
from django.test import Client


class JerseyTest(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        # creating instance of a client.
        self.client = Client()
        logged_in = self.client.login(username='www', password='$3cureUS')

    def test_createUser(self):
        response = self.client.post(
            '/jersey/api/v1/User/create',
            {
                'email': 'l.da@gmail.com',
                'first_name': 'Leonardo',
                'last_name': 'DaVinci',
                'shirt_size': 'XXL',
            })

        self.assertEqual(response.status_code, 201)

    def test_createJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'ExampleTeam',
                'number': '1',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
            })

        self.assertEqual(response.status_code, 201)

    def test_updateJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/1/update',
            {
                'team': 'NewTeam',
                'number': '2',
                'player': 'Michael Chang',
                'shirt_size': 'M',
                'primary_color': 'White',
                'secondary_color': 'Black',
            })
        self.assertEqual(response.status_code, 200)

    def test_updateUser(self):
        response = self.client.post(
            '/jersey/api/v1/User/1/update',
            {
                'email': 'myc6cp@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
            })
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
# Create your tests here.
