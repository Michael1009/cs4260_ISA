from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import urllib.request
from django.core.serializers.json import DjangoJSONEncoder
from kafka import KafkaProducer


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
        data = None
        result = None
        try:
            preform_data = {
                "email": request.POST.get("email"),
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "password": request.POST.get("password"),
                "shirt_size": request.POST.get("shirt_size")
                }
            data = urllib.parse.urlencode(preform_data).encode("utf-8")
        except Exception as e:
            result = json.dumps(
            {'message': 'Missing field or malformed data in CREATE request. Caught at exp layer. Here is the data we received: {}'.format(data),
            'ok': False,})

        try: 
            url = 'http://models:8000/jersey/api/v1/users/register'
            req = urllib.request.Request(url, data=data, method='POST')

            json_response = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)
            result = json_dump
        except Exception as e:
            result = json.dumps(
                {'error': 'REGISTER: Missing field or malformed data in POST request.', 'ok': False, 'data':request.POST, 'exception': str(e)}
            )
        return HttpResponse(result, content_type='application/json')  

@csrf_exempt
def login(request):
    if request.method == "POST":
        url = 'http://models:8000/jersey/api/v1/users/login'
        try: 
            preform_data = {
                "email": request.POST.get("email"),
                "password": request.POST.get("password")
            }
            get_post_encoded = urllib.parse.urlencode(preform_data).encode('utf-8')

            URLrequest = urllib.request.Request(url, data=get_post_encoded, method='POST')

            json_response = urllib.request.urlopen(URLrequest).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)
            return HttpResponse(json_dump, content_type='applications/json')
        except Exception as e:
            result = json.dumps(
            {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(request.POST), 
            'ok': False,
            'exception': str(e)
            })
            return HttpResponse(result, content_type='application/json')  

@csrf_exempt 
def info(request):
    if request.method == "POST":
        url = 'http://models.:8000/jersey/api/v1/info'
        data=None
        try: 
            preform_data = {
                "auth": request.POST.get("auth")
            }
            data = urllib.parse.urlencode(preform_data).encode("utf-8")
        except Exception as e:
            result = json.dumps(
            {'message': 'Missing field or malformed data in CREATE request. Caught at exp layer. Here is the data we received: {}'.format(data),
            'ok': False,})
        try: 
            req = urllib.request.Request(url, data=data, method='POST')
            json_response = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)
            result = json_dump
        except Exception as e:
            result = json.dumps(
                {'error': 'REGISTER: Missing field or malformed data in POST request.', 'ok': False, 'data':data.decode('utf-8'), 'exception': str(e)}
            )
        return HttpResponse(result, content_type='application/json')  

@csrf_exempt
def create_item(request):
    if request.method == "POST":
        url = 'http://models:8000/jersey/api/v1/Jersey/create'
        data = None
        result = None
        try: 
            preform_data = {
                "authenticator": request.POST.get("authenticator"),
                "team": request.POST.get("team"),
                "player": request.POST.get("player"),
                "number": request.POST.get("number"),
                "shirt_size": request.POST.get("shirt_size"),
                "primary_color": request.POST.get("primary_color"),
                "secondary_color": request.POST.get("secondary_color"),
            }
            data = urllib.parse.urlencode(preform_data).encode("utf-8")
        except Exception as e:
            result = json.dumps({
                'message': 'Missing field or malformed data in creating a listing. Caught at exp layer. Here is the data we received: {}'.format(request.POST),
                'ok': False,
                'exception':str(e)
            })
        try:
            req = urllib.request.Request(url,data=data,method="POST")
            json_response = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(json_response)
            json_dump = json.dumps(resp)
            result = json_dump
           
        except Exception as e:
            result = json.dumps({
                'error': 'REGISTER: Missing field or malformed data in POST request.', 
                'ok': False, 
                'data':data.decode('utf-8'), 
                'exception': str(e)
            })
        producer = KafkaProducer(bootstrap_servers='kafka:9092')
        producer.send('new-items-topic', json.dumps(resp['result']).encode('utf-8'))
        return HttpResponse(result, content_type='application/json')  