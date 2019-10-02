from django.test import TestCase
from django.test import Client
from django.core import serializers
from .models import User, Jersey


class JerseyTest(TestCase):

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        # creating instance of a client.
        self.client = Client()
        logged_in = self.client.login(username='www', password='$3cureUS')

        Jersey.objects.create(team="ExampleTeam_1", number="1", player="Bob Dylan",
                              shirt_size="M", primary_color="White", secondary_color="Black")

    def test_createJersey_InvalidMethod(self):
        response = self.client.get('/jersey/api/v1/Jersey/create')
        self.assertEqual(response.status_code, 400)

    def test_createJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'ExampleTeam_2',
                'number': '2',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
            })
        self.assertEqual(response.status_code, 200)

    def test_createJersey_MalformedRequest(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'ExampleTeam_2',
            })
        self.assertEqual(response.status_code, 400)

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

    def test_updateJersey_MalformedRequest(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/1/update',
            {
                'team': 'NewTeam',
            })
        self.assertEqual(response.status_code, 400)

    def test_updateJersey_InvalidID(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/99/update',
            {
                'team': 'NewTeam',
                'number': '2',
                'player': 'Michael Chang',
                'shirt_size': 'M',
                'primary_color': 'White',
                'secondary_color': 'Black',
            })
        self.assertEqual(response.status_code, 404)

    def test_getJersey(self):
        response = self.client.get('/jersey/api/v1/Jersey/1')
        obj = serializers.serialize("json", [Jersey.objects.get(pk=1)])
        self.assertContains(response, obj)

    def test_getJersey_InvalidID(self):
        response = self.client.get('/jersey/api/v1/Jersey/99')
        self.assertEqual(response.status_code, 404)

    def test_getAllJerseys(self):
        response = self.client.get('/jersey/api/v1/Jersey')
        objects = serializers.serialize("json", Jersey.objects.all())
        self.assertContains(response, objects)

    def test_deleteJersey(self):
        response = self.client.delete('/jersey/api/v1/Jersey/1/delete')
        self.assertEquals(response.status_code, 200)

    def test_deleteJersey_InvalidID(self):
        response = self.client.delete('/jersey/api/v1/Jersey/99/delete')
        self.assertEquals(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class UserTest(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        # creating instance of a client.
        self.client = Client()
        logged_in = self.client.login(username='www', password='$3cureUS')

        User.objects.create(email="myc6cp@virginia.edu",
                            first_name="Michael", last_name="Chang", shirt_size="M")

    def test_createUser_InvalidMethod(self):
        response = self.client.get('/jersey/api/v1/User/create')
        self.assertEqual(response.status_code, 400)

    def test_createUser(self):
        response = self.client.post(
            '/jersey/api/v1/User/create',
            {
                'email': 'l.da@gmail.com',
                'first_name': 'Leonardo',
                'last_name': 'DaVinci',
                'shirt_size': 'XXL',
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

    def test_updateUser_MalformedRequest(self):
        response = self.client.post(
            '/jersey/api/v1/User/1/update',
            {
                'email': 'myc6cp@gmail.com',
            })
        self.assertEqual(response.status_code, 400)

    def test_updateUser_InvalidID(self):
        response = self.client.post(
            '/jersey/api/v1/User/99/update',
            {
                'email': 'myc6cp@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
            })
        self.assertEqual(response.status_code, 404)

    def test_getUser(self):
        response = self.client.get('/jersey/api/v1/User/1')
        obj = serializers.serialize("json", [User.objects.get(pk=1)])
        self.assertContains(response, obj)

    def test_getUser_InvalidID(self):
        response = self.client.get('/jersey/api/v1/User/99')
        self.assertEqual(response.status_code, 404)

    def test_getAllUsers(self):
        response = self.client.get('/jersey/api/v1/User')
        objects = serializers.serialize("json", User.objects.all())
        self.assertContains(response, objects)

    def test_deleteUser(self):
        response = self.client.delete('/jersey/api/v1/User/1/delete')
        self.assertEquals(response.status_code, 200)

    def test_deleteUser_InvalidID(self):
        response = self.client.delete('/jersey/api/v1/User/99/delete')
        self.assertEquals(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
