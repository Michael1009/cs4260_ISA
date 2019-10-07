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
        data = json.dumps(response.read().decode('UTF-8'))
    result = json.loads(data)
    return HttpResponse(result)


@csrf_exempt
def jersey_detail(request, id):
    data = None
    try:
        with urllib.request.urlopen('http://models:8000/jersey/api/v1/Jersey/'+str(id)) as response:
            data = json.dumps(response.read().decode('UTF-8'))
    except:
        result = json.dumps(
            {'error': '404', 'ok': False})
        return HttpResponse(result, content_type='application/json', status=404)
    result = json.loads(data)
    return HttpResponse(result)
