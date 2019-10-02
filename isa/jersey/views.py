from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import User, Jersey
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Hello, world. You're at the jersey index.")


def incorrect_REST_method(method):
    result = json.dumps(
        {'error': 'Incorrect REST method used. This endpoint expects a {} request'.format(method), 'ok': False})
    return HttpResponse(result, status=400)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        form = request.POST
        try:
            new_user = User(
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                shirt_size=request.POST['shirt_size']
            )
            new_user.save()
            result = json.dumps({'ok': True})
            return HttpResponse(result, status=200)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form), 'ok': False})
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")


@csrf_exempt
def create_jersey(request):
    if request.method == "POST":
        try:
            new_jersey = Jersey(
                team=request.POST['team'],
                number=request.POST['number'],
                player=request.POST['player'],
                shirt_size=request.POST['shirt_size'],
                primary_color=request.POST['primary_color'],
                secondary_color=request.POST['secondary_color']
            )
            new_jersey.save()
            result = json.dumps({'ok': True})
            return HttpResponse(result, status=200)
        except:
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request.', 'ok': False})
            return HttpResponse(result, status=400)
    else:
        return incorrect_REST_method("POST")


def update(request, model, id):
    try:
        obj = model.objects.get(pk=id)
        if model == Jersey:
            try:
                obj.team = request.POST['team']
                obj.number = request.POST['number']
                obj.player = request.POST['player']
                obj.shirt_size = request.POST['shirt_size']
                obj.primary_color = request.POST['primary_color']
                obj.secondary_color = request.POST['secondary_color']
            except:
                result = json.dumps(
                    {'error': 'Missing field or malformed data in POST request.', 'ok': False})
                return HttpResponse(result, status=400)
        elif model == User:
            try:
                obj.email = request.POST['email']
                obj.first_name = request.POST['first_name']
                obj.last_name = request.POST['last_name']
                obj.shirt_size = request.POST['shirt_size']
            except:
                result = json.dumps(
                    {'error': 'Missing field or malformed data in POST request.', 'ok': False})
                return HttpResponse(result, status=400)
        obj.save()
        result = json.dumps({'ok': True})
        return HttpResponse(result, status=200)
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
        response = serializers.serialize("json", model.objects.all())
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
