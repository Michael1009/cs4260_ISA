from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
import urllib.request


def incorrect_REST_method(method):
    result = json.dumps(
        {'error': 'Incorrect REST method used. This endpoint expects a {} request'.format(method), 'ok': False})
    return HttpResponse(result)


@csrf_exempt
def home(request):
    data = None
    with urllib.request.urlopen('http://app_models_1:8000/jersey/api/v1/Jersey') as response:
        data = response.read()

    return HttpResponse(json.loads(data.decode('utf8')))


@csrf_exempt
def jersey_detail(request):
    return HttpResponse('Could not save data')
