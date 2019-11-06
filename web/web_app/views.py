from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
import urllib.request
import json
from collections import OrderedDict
from django.template.context_processors import csrf
from web_app.forms import RegisterForm, LoginForm, CreateJerseyForm
# Create your views here.


def index(request):
    data = None
    with urllib.request.urlopen('http://exp:8000/exp/home/') as response:
        data = response.read().decode('UTF-8')
    myList = {}
    i = 0
    for loop1 in json.loads(data):
        bigData = json.loads(data)[i]['fields']
        myList[json.loads(data)[i]['pk']] = bigData
        i = i + 1
    # I reverse sorted the dictionaries because order_by doesn't seem to be working
    # essentially, the first item in this new dict is the last thing put into the database
    sorted_dictionary = OrderedDict(
        sorted(myList.items(), key=lambda v: v, reverse=True))
    context = {
        'jerseys': sorted_dictionary,
    }
    if request.GET.get('already_logged_in'):
        context['already_logged_in'] = True
    return render(request, 'web_app/index.html', context)


def jersey_by_size(request, size):
    data = None
    with urllib.request.urlopen('http://exp:8000/exp/home/'+size) as response:
        data = response.read().decode('UTF-8')
    myList = {}
    i = 0
    for loop1 in json.loads(data):
        bigData = json.loads(data)[i]['fields']
        myList[json.loads(data)[i]['pk']] = bigData
        i = i + 1
    context = {
        'jerseys': myList
    }
    return render(request, 'web_app/index.html', context)


def item_detail(request, id):
    user_id = request.COOKIES.get('user_id')
    data = None
    template = None
    context = None
    url = 'http://exp:8000/exp/jersey_detail/'+str(id)
    if user_id:
        url = url + "/" + user_id
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('UTF-8')
    json_data = json.loads(data)
    if 'error' in json_data:
        template = '404.html'
    else:
        template = 'web_app/item_detail.html'
        context = {
            'jersey': json_data[0]['fields']
        }
    return render(request, template, context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            shirt_size = form.cleaned_data['shirt_size']

            register_data = {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "password": password,
                "shirt_size": shirt_size
            }

            data = urllib.parse.urlencode(register_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/exp/users/register/')
            with urllib.request.urlopen(req, data=data) as f:
                resp = f.read()

            resp_text = resp.decode('utf-8')
            resp_dict = json.loads(resp_text)

            context = {}
            if not resp or not resp_dict['ok']:
                context['error'] = resp_dict['error']
                context['form'] = form
                return render(request, 'web_app/register.html', context)

            authenticator = resp_dict['authenticator']
            response = HttpResponseRedirect('/')

            response.set_cookie("user_id", resp_dict['user_id'])
            response.set_cookie("auth", authenticator)
            return response
        else:
            return render(request, 'web_app/register.html', {'form': form, })
    else:
        form = RegisterForm()
    return render(request, 'web_app/register.html', {'form': form, 'get': True})
    # return HttpResponse("<h1> Hello World </h1>")


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # cleaning the data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            login_data = {"email": email, "password": password}
            data_encoded = urllib.parse.urlencode(login_data).encode('utf-8')
            # our next page
            next = reverse('index')
            resp = urllib.request.Request(
                'http://exp:8000/exp/users/login/', data=data_encoded, method='POST')
            #resp_json = json.dumps(resp)
            req = urllib.request.urlopen(resp).read().decode('utf-8')
            resp_json = json.loads(req)
            if not resp or not resp_json['ok']:
                # todo figure out how to display possible errors here
                return render(request, 'web_app/login.html', {'form': form, 'message': "Invalid login. Please try again"})

            # at this point we can log them in
            authenticator = resp_json['authenticator']
            response = HttpResponseRedirect(reverse('index'))
            if 'next' in request.POST:
                response = HttpResponseRedirect(
                    reverse(request.POST.get('next')))

            response.set_cookie("user_id", resp_json['user_id'])
            response.set_cookie("auth", authenticator)
            return response
        else:
            return render(request, 'web_app/login.html', {'form': form})
    else:
        if request.COOKIES.get('auth'):
            base_url = reverse('index')
            query_string = urllib.parse.urlencode(
                {'already_logged_in': True})
            url = '{}?{}'.format(base_url, query_string)
            return HttpResponseRedirect(url)
        form = LoginForm()
        context = {'form': form}
        if request.GET.get('redirect_create'):
            context['redirect_create'] = True
    return render(request, 'web_app/login.html', context)


def logout(request):
    response = HttpResponseRedirect(reverse('index'))
    response.delete_cookie('auth')
    return response


def create_jersey(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        base_url = reverse('login_page')
        query_string = urllib.parse.urlencode(
            {'redirect_create': True, 'next': 'create_jersey'})
        url = '{}?{}'.format(base_url, query_string)
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        form = CreateJerseyForm(request.POST)
        if form.is_valid():
            # cleaning the data
            authenticator = auth
            team = form.cleaned_data['team']
            number = form.cleaned_data['number']
            player = form.cleaned_data['player']
            shirt_size = form.cleaned_data['shirt_size']
            primary_color = form.cleaned_data['primary_color']
            secondary_color = form.cleaned_data['secondary_color']

            jersey_data = {
                "authenticator": authenticator,
                "team": team,
                "number": number,
                "player": player,
                "shirt_size": shirt_size,
                "primary_color": primary_color,
                "secondary_color": secondary_color
            }
            data_encoded = urllib.parse.urlencode(jersey_data).encode('utf-8')

            resp = urllib.request.Request(
                'http://exp:8000/exp/users/create_item/', data=data_encoded, method='POST')
            req = urllib.request.urlopen(resp).read().decode('utf-8')
            resp_json = json.loads(req)
            if not resp or not resp_json['ok']:
                    # todo figure out how to display possible errors here
                return render(request, 'web_app/login.html', {'form': form})
                #new_item = resp['result']['id']
                # url = 'http://exp-api:8000/api/jersey_detail/'{}/'.format(new_item)
                #resp_json = urllib.request.urlopen(url).read().decode('utf-8')
                #resp = json.loads(resp_json)
            response = HttpResponseRedirect(reverse('index'))
            return response
    else:
        form = CreateJerseyForm()
    return render(request, 'web_app/create_jersey.html', {'form': form})

def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        encoded = urllib.parse.urlencode({'query': query})
        url = 'http://exp:8000/exp/search/?{}'.format(encoded)
        resp_json = urllib.request.urlopen(url).read().decode('utf-8')
        resp = json.loads(resp_json)
        ok_check = resp['ok']
        result = []
        if 'result' in resp:
            result = [i['_source'] for i in resp['result']]
        #auth = request.COOKIES.get('authenticator')
        #if auth:
            #['logged_in'] = True
        # need to check if login is valid ... 
        return render(request, 'search.html', {'ok': ok_check, 'query': query, 'items': result})
