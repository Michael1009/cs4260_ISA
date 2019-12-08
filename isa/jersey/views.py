from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import User, Jersey, Authenticator, Recommendation
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import make_password, check_password
import os
import hmac
# import django settings file
from django.conf import settings
import datetime


def index(request):
    return HttpResponse("Hello, world. You're at the jersey index.")


def incorrect_REST_method(method):
    result = json.dumps(
        {'error': 'Incorrect REST method used. This endpoint expects a {} request'.format(method), 'ok': False})
    return HttpResponse(result, status=400)

##### CRUD #####
@csrf_exempt
def create_jersey(request):
    if request.method == "POST":
        try:
            post_data = request.POST
            auth_val = post_data['authenticator']
            auth_obj = Authenticator.objects.get(authenticator=auth_val)
            user_obj = auth_obj.user_id
            user = user_obj
            #user = User.objects.get(email=request.POST['user_id'])
            auth = auth_obj
            if auth.authenticator == request.POST['authenticator']:
                new_jersey = Jersey(
                    team=request.POST['team'],
                    number=request.POST['number'],
                    player=request.POST['player'],
                    shirt_size=request.POST['shirt_size'],
                    primary_color=request.POST['primary_color'],
                    secondary_color=request.POST['secondary_color'],
                    user_id=user,
                )
                new_jersey.save()

                new_jersey_json_string = serializers.serialize(
                    'json', [new_jersey, ])
                new_jersey_json = json.loads(new_jersey_json_string)
                result = json.dumps({'ok': True, 'jersey': new_jersey_json[0]})
                return HttpResponse(result, status=200)
            else:
                result = json.dumps(
                    {'error': 'Create Jersey: Not authorized', 'ok': False})
                return HttpResponse(result, status=401)
        except KeyError as e:
            result = json.dumps(
                {'error': 'Create Jersey: Missing field or malformed data in POST request.',
                 'ok': False,
                 'exception': str(e)}
            )
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")

def create_recommendation(request): 
    if request.method == "POST":
        try:
            post_data = request.POST
            new_recommendation = Recommendation(
                item_being_viewed = post_data['item_being_viewed'],
                recommended_items = post_data['recommended_items']
            )
            new_recommendation.save()
            result = json.dumps({'ok': True, 'recommendation': json.loads(new_recommendation)[0]})
            return HttpResponse(result, status=200)
        except KeyError as e:
            result = json.dumps(
                {'error': 'Create Recommendation: Missing field or malformed data in POST request.',
                 'ok': False,
                 'exception': str(e)}
            )
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")

def update(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        user = User.objects.get(email=request.POST['user_id'])
        auth = Authenticator.objects.get(user_id=user)
        if auth.authenticator == request.POST['authenticator']:
            if model == Jersey:
                try:
                    obj.team = request.POST['team']
                    obj.number = request.POST['number']
                    obj.player = request.POST['player']
                    obj.shirt_size = request.POST['shirt_size']
                    obj.primary_color = request.POST['primary_color']
                    obj.secondary_color = request.POST['secondary_color']
                    obj.user_id = user

                except:
                    result = json.dumps(
                        {'error': 'Update Jersey: Missing field or malformed data in POST request.', 'ok': False})
                    return HttpResponse(result, status=400)
            elif model == User:
                try:
                    obj.email = request.POST['email']
                    obj.first_name = request.POST['first_name']
                    obj.last_name = request.POST['last_name']
                    obj.shirt_size = request.POST['shirt_size']
                except:
                    result = json.dumps(
                        {'error': 'Update User: Missing field or malformed data in POST request.', 'ok': False})
                    return HttpResponse(result, status=400)
            obj.save()
            result = json.dumps({'ok': True})
            return HttpResponse(result, status=200)
        else:
            result = json.dumps(
                {'error': 'Update: Unauthorized.', 'ok': False})
            return HttpResponse(result, status=401)
    except:
        result = json.dumps(
            {'error': 'Invalid Id in POST request.', 'ok': False})
        return HttpResponse(result, content_type='application/json', status=404)


@csrf_exempt
def update_jersey(request, id):
    if request.method == "POST":
        return update(request, Jersey, id)
    else:
        return incorrect_REST_method("POST")


@csrf_exempt
def update_user(request, id):
    if request.method == "POST":
        return update(request, User, id)
    else:
        return incorrect_REST_method("POST")


def delete_data(model, id):
    try:
        obj = model.objects.get(pk=id)
        obj.delete()
        result = json.dumps({'ok': True})
        return HttpResponse(result, content_type='application/json', status=200)
    except model.DoesNotExist:
        result = json.dumps(
            {'error': '{} with id={} not found'.format(model, id), 'ok': False})
        return HttpResponse(result, content_type='application/json', status=404)


@csrf_exempt
def delete_user(request, id):
    if request.method == "DELETE":
        return delete_data(User, id)
    return incorrect_REST_method("DELETE")

@csrf_exempt
def delete_user_by_email(request,email):
    if request.method == "DELETE":
        try:
            cur_id = User.objects.get(email=email).id
            Jersey.objects.filter(user_id = cur_id).delete()
            User.objects.get(email=email).delete()
            response  = {
                'ok': True,
                'message': "{} deleted".format(email)
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)

        except:
            response = {
                'ok': False,
                'error': "Unable to delete specified user",
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=200)
    else:
        return incorrect_REST_method("DELETE")


@csrf_exempt
def delete_jersey(request, id):
    if request.method == "DELETE":
        return delete_data(Jersey, id)
    return incorrect_REST_method("DELETE")


def get_data(model, args):
    try:
        id = args['id']
        obj = model.objects.get(pk=id)
        response = serializers.serialize("json", [obj])
        return HttpResponse(response, content_type='application/json', status=200)
    except:
        id = args['id']
        response = json.dumps(
            {'error': '{} with id={} not found'.format(model, id), 'ok': False})
        return HttpResponse(response, content_type='application/json', status=404)


def get_all_data(model, args):
    try:
        response = serializers.serialize(
            "json", model.objects.all().order_by('id'))
        return HttpResponse(response, content_type='application/json', status=200)
    except:
        response = json.dumps(
            {'error': 'Was not able to get data', 'ok': False})
        return HttpResponse(response, content_type='application/json', status=404)


@csrf_exempt
def get_user(request, **kwargs):
    if request.method == "GET":
        return get_data(User, kwargs)
    return incorrect_REST_method("GET")


@csrf_exempt
def get_jersey(request, **kwargs):
    if request.method == "GET":
        return get_data(Jersey, kwargs)
    return incorrect_REST_method("GET")


@csrf_exempt
def get_all_user(request, **kwargs):
    if request.method == "GET":
        return get_all_data(User, kwargs)
    return incorrect_REST_method("GET")


def get_all_jersey(request, **kwargs):
    if request.method == "GET":
        return get_all_data(Jersey, kwargs)
    return incorrect_REST_method("GET")


def get_jersey_by_size(request, **kwargs):
    if request.method == "GET":
        return get_all_data_by_size(Jersey, kwargs)
    return incorrect_REST_method("GET")

# id is the id of the jersey you want recommendations for
def get_recommendations(request, id):
    if request.method == "GET":
        try:
            obj = Recommendation.objects.get(item_being_viewed=id)
            response = serializers.serialize("json", [obj])
            return HttpResponse(response, content_type='application/json', status=200)
        except:
            response = json.dumps(
                {'error': 'Recommendation for jersey id {} not found'.format(id), 'ok': False})
            return HttpResponse(response, content_type='application/json', status=404)
    return incorrect_REST_method("GET")


def get_all_data_by_size(model, args):
    try:
        if args['size'] == "small":
            data = model.objects.filter(shirt_size="S")
            response = serializers.serialize("json", data)
            return HttpResponse(response, content_type='application/json', status=200)
        if args['size'] == "medium":
            data = model.objects.filter(shirt_size="M")
            response = serializers.serialize("json", data)
            return HttpResponse(response, content_type='application/json', status=200)
        if args['size'] == 'large':
            data = model.objects.filter(shirt_size="L")
            response = serializers.serialize("json", data)
            return HttpResponse(response, content_type='application/json', status=200)
        data = model.objects.filter(shirt_size="L")
        response = serializers.serialize("json", data)
        return HttpResponse(response, content_type='application/json', status=200)
    except:
        response = json.dumps(
            {'error': 'Was not able to get data', 'ok': False})
        return HttpResponse(response, content_type='application/json', status=404)

##### Authentication #####


def jsonResponse(dic=None):
    if dic == None:
        result = json.dumps({'ok': True})
    else:
        result = json.dumps({'result': dic, 'ok': True}, cls=DjangoJSONEncoder)
    return HttpResponse(result, content_type='application/json')


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])

            # If valid password, create authenticator and return success
            if check_password(request.POST['password'], user.password):
                # Create Authenticator
                authenticator = None
                try:
                    authenticator = create_authenticator(user)
                except:
                    result = json.dumps(
                        {'error': 'LOGIN: Create Authenticator Failed', 'ok': False})
                    return HttpResponse(result, status=400)

                result = json.dumps(
                    {'ok': True, 'authenticator': authenticator, 'user_id': request.POST['email']})
                return HttpResponse(result, status=200)
            else:
                result = json.dumps(
                    {'error': 'LOGIN: User is not authorized', 'ok': False})
                return HttpResponse(result, status=401)
        except:
            result = json.dumps(
                {'error': 'LOGIN: Cannot find User.', 'ok': False})
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            user_count = User.objects.filter(
                email=request.POST['email']).count()
            if user_count == 0:
                new_user = User(
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    password=make_password(request.POST['password']),
                    shirt_size=request.POST['shirt_size'],
                )
                new_user.save()
                # Create Authenticator
                authenticator = None
                try:
                    authenticator = create_authenticator(new_user)
                except Exception as e:
                    result = json.dumps(
                        {'error': 'REGISTER: Create Authenticator Failed', 'ok': False})
                    return HttpResponse(str(e), status=400)

                result = json.dumps(
                    {'ok': True, 'authenticator': authenticator, 'user_id': request.POST['email']})
                return HttpResponse(result, status=200)
            else:
                result = json.dumps(
                    {'error': 'REGISTER: User already exists', 'ok': False})
                return HttpResponse(result, status=200)
        except Exception as e:
            result = json.dumps(
                {'error': 'REGISTER: Missing field or malformed data in POST request.', 'ok': False, 'data': request.POST, 'exception': str(e)})
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")


@csrf_exempt
def create_authenticator(user):
    authenticator = hmac.new(
        key=settings.SECRET_KEY.encode('utf-8'),
        msg=os.urandom(32),
        digestmod='sha256',
    ).hexdigest()
    # Clear out any old Auth
    auth_count = Authenticator.objects.filter(
        user_id=user).count()
    if auth_count == 1:
        last_auth = Authenticator.objects.get(user_id=user)
        last_auth.delete()
    # Create new one
    new_authenticator = Authenticator(
        user_id=user,
        authenticator=authenticator,
    )
    new_authenticator.save()
    return authenticator


@csrf_exempt
def logout(request):
    if request.method == "POST":
        try:
            auth_val = request.POST['auth']
            auth_obj = Authenticator.objects.get(authenticator=auth_val)
            auth_obj.delete()
            result = json.dumps({'ok': True})
            return HttpResponse(result, status=200)
        except:
            result = json.dumps(
                {'error': 'LOGOUT: Cannot find auth.', 'ok': False})
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")


@csrf_exempt
def info(request):
    # use auth to get user and subsequently their info
    if request.method == "POST":
        try:
            post_data = request.POST
            auth_val = post_data['auth']
            auth_obj = Authenticator.objects.get(authenticator=auth_val)
            user_obj = auth_obj.user_id
            result = json.dumps({
                'first_name': user_obj.first_name,
                'last_name': user_obj.last_name,
                'email': user_obj.email,
                'shirt_size': user_obj.shirt_size
            })
            return HttpResponse(result, status=200)
        except Exception as e:
            result = json.dumps(
                {'error': 'REGISTER: Missing field or malformed data in POST request.', 'ok': False, 'data': request.POST, 'exception': str(e)})
            return HttpResponse(result, status=400)


