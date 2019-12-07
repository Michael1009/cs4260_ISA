from django.test import TestCase
from django.test import Client
from django.core import serializers
from .models import User, Jersey, Authenticator
import urllib.request
import json


class JerseyTest(TestCase):
    auth = ''
    user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # creating instance of a client.
        cls.client = Client()
        logged_in = cls.client.login(username='www', password='$3cureUS')
        response = cls.client.post(
            '/jersey/api/v1/users/register',
            {
                'email': 'test@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'password': 'test'
            })
        resp_json = json.loads(response.content.decode('utf-8'))
        cls.auth = resp_json['authenticator']
        cls.user = User.objects.get(email='test@gmail.com')

    def test_createJersey_InvalidMethod(self):
        response = self.client.get('/jersey/api/v1/Jersey/create')
        self.assertEqual(response.status_code, 400)

    def test_createJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'TestTeam',
                'number': '2',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
                'authenticator': self.auth,
                'user_id': self.user.email
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
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'TestTeam',
                'number': '2',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        jersey = Jersey.objects.get(team='TestTeam')

        response = self.client.post(
            '/jersey/api/v1/Jersey/'+str(jersey.id)+'/update',
            {
                'team': 'NewTeam',
                'number': '2',
                'player': 'Michael Chang',
                'shirt_size': 'M',
                'primary_color': 'White',
                'secondary_color': 'Black',
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        self.assertEqual(response.status_code, 200)

    def test_updateJersey_MalformedRequest(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/1/update',
            {
                'team': 'NewTeam',
            })
        self.assertEqual(response.status_code, 404)

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
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        self.assertEqual(response.status_code, 404)

    def test_getJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'TestTeam',
                'number': '2',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        jersey = Jersey.objects.get(team='TestTeam')

        response = self.client.get('/jersey/api/v1/Jersey/'+str(jersey.id))
        obj = serializers.serialize("json", [jersey])
        self.assertContains(response, obj)

    def test_getJersey_InvalidID(self):
        response = self.client.get('/jersey/api/v1/Jersey/99')
        self.assertEqual(response.status_code, 404)

    def test_getAllJerseys(self):
        response = self.client.get('/jersey/api/v1/Jersey')
        objects = serializers.serialize("json", Jersey.objects.all())
        self.assertContains(response, objects)

    def test_deleteJersey(self):
        response = self.client.post(
            '/jersey/api/v1/Jersey/create',
            {
                'team': 'TestTeam',
                'number': '2',
                'player': 'Leonardo DaVinci',
                'shirt_size': 'XXL',
                'primary_color': 'White',
                'secondary_color': 'Black',
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        jersey = Jersey.objects.get(team='TestTeam')
        response = self.client.delete(
            '/jersey/api/v1/Jersey/'+str(jersey.id)+'/delete')
        self.assertEquals(response.status_code, 200)

    def test_deleteJersey_InvalidID(self):
        response = self.client.delete('/jersey/api/v1/Jersey/99/delete')
        self.assertEquals(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class UserTest(TestCase):
    auth = ''
    user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # creating instance of a client.
        cls.client = Client()
        logged_in = cls.client.login(username='www', password='$3cureUS')
        response = cls.client.post(
            '/jersey/api/v1/users/register',
            {
                'email': 'test@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'password': 'test'
            })
        resp_json = json.loads(response.content.decode('utf-8'))
        cls.auth = resp_json['authenticator']
        cls.user = User.objects.get(email='test@gmail.com')

    def test_updateUser(self):
        response = self.client.post(
            '/jersey/api/v1/User/'+str(self.user.id)+'/update',
            {
                'email': 'myc6cp@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'authenticator': self.auth,
                'user_id': self.user.email
            })
        self.assertEqual(response.status_code, 200)

    def test_updateUser_MalformedRequest(self):
        response = self.client.post(
            '/jersey/api/v1/User/1/update',
            {
                'email': 'myc6cp@gmail.com',
            })
        self.assertEqual(response.status_code, 404)

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
        response = self.client.get('/jersey/api/v1/User/'+str(self.user.id))
        obj = serializers.serialize("json", [self.user])
        self.assertContains(response, obj)

    def test_getUser_InvalidID(self):
        response = self.client.get('/jersey/api/v1/User/99')
        self.assertEqual(response.status_code, 404)

    def test_getAllUsers(self):
        response = self.client.get('/jersey/api/v1/User')
        objects = serializers.serialize("json", User.objects.all())
        self.assertContains(response, objects)

    def test_deleteUser(self):
        response = self.client.delete(
            '/jersey/api/v1/User/'+str(self.user.id)+'/delete')
        self.assertEquals(response.status_code, 200)

    def test_deleteUser_InvalidID(self):
        response = self.client.delete('/jersey/api/v1/User/99/delete')
        self.assertEquals(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()


class AuthTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # creating instance of a client.
        cls.client = Client()
        logged_in = cls.client.login(username='www', password='$3cureUS')

    def test_register(self):
        response = self.client.post(
            '/jersey/api/v1/users/register',
            {
                'email': 'test@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'password': 'test'
            })
        user = User.objects.get(email='test@gmail.com')
        resp_json = json.loads(response.content.decode('utf-8'))
        auth = resp_json['authenticator']
        auth_obj = Authenticator.objects.get(user_id=user)
        self.assertEqual(auth, auth_obj.authenticator)
        self.assertEqual(response.status_code, 200)

    def test_register_InvalidMethod(self):
        response = self.client.get('/jersey/api/v1/users/register')
        self.assertEqual(response.status_code, 400)

    def test_register_MalformedRequest(self):
        response = self.client.post('/jersey/api/v1/users/register')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        response = self.client.post(
            '/jersey/api/v1/users/register',
            {
                'email': 'test@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'password': 'test'
            })
        resp_json = json.loads(response.content.decode('utf-8'))
        auth_1 = resp_json['authenticator']
        response = self.client.post(
            '/jersey/api/v1/users/logout',
            {
                'auth': auth_1
            })
        response = self.client.post(
            '/jersey/api/v1/users/login',
            {
                'email': 'test@gmail.com',
                'password': 'test'
            })
        user = User.objects.get(email='test@gmail.com')
        resp_json = json.loads(response.content.decode('utf-8'))
        auth_2 = resp_json['authenticator']
        auth_obj = Authenticator.objects.get(user_id=user)
        self.assertNotEqual(auth_1, auth_2)
        self.assertEqual(auth_2, auth_obj.authenticator)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.post(
            '/jersey/api/v1/users/register',
            {
                'email': 'test@gmail.com',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'shirt_size': 'M',
                'password': 'test'
            })
        resp_json = json.loads(response.content.decode('utf-8'))
        auth = resp_json['authenticator']
        response = self.client.post(
            '/jersey/api/v1/users/logout',
            {
                'auth': auth
            })
        auth_count = Authenticator.objects.filter(
            authenticator=auth).count()
        self.assertEqual(0, auth_count)
        self.assertEqual(response.status_code, 200)
