from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from django.core.serializers.json import DjangoJSONEncoder


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
def jersey_by_size(request,size):
    data = None
    with urllib.request.urlopen('http://models:8000/jersey/api/v1/Jersey/'+size) as response:
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
        return HttpResponse(result, content_type='application/json', status=200)
    result = json.loads(data)
    return HttpResponse(result)

@csrf_exempt 
def register(request): 
    if request.method == "POST":
        try:
            preform_data = {
                "email": request.POST.get("email"),
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "password": request.POST.get("password"),
                "shirt_size": request.POST.get("shirt_size")
                }
            data = urllib.parse.urlencode(preform_data).encode("utf-8")
            url = 'http://models:8000/jersey/api/v1/users/register'
    

            request = urllib.request.Request(url, data=data, method='POST')

            json_response = urllib.request.urlopen(request).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)

            return HttpResponse(json_dump)
        except Exception as e:
            result = json.dumps(
            {'error': 'Missing field or malformed data in CREATE request. Caught at exp layer. Here is the data we received: {}'.format(data), 'ok': False, 'exception': str(e)})
            return HttpResponse(result, content_type='application/json')  

@csrf_exempt 
def login(request):
    if request.method == "POST":
        get_post_data = request.POST
        try: 
            url = 'http://models.:8000/jersey/api/v1/users/login'
            get_post_encoded = urllib.parse.urlencode(get_post_data).encode('utf-8')

            request = urllib.request.Request(url, data=get_post_encoded, method='POST')

            json_response = urllib.request.urlopen(request).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)
            return HttpRespose(json_dump)
        except:
            result = json.dumps(
            {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(get_post_data), 'ok': False})
            return HttpResponse(result, content_type='application/json')  