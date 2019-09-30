from django.http import HttpResponse
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
    with urllib.request.urlopen('http://models:8000/jersey/api/v1/Jersey') as response:
        data = response.read().decode('UTF-8')
    return HttpResponse(json.loads(data))


@csrf_exempt
def jersey_detail(request, id):
    data = None
    with urllib.request.urlopen('http://models:8000/jersey/api/v1/Jersey/'+str(id)) as response:
        data = response.read().decode('UTF-8')
    return HttpResponse(json.loads(data))
