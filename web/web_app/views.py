from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
import urllib.request, json
from collections import OrderedDict

from web_app.forms import RegisterForm, LoginForm
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
    #I reverse sorted the dictionaries because order_by doesn't seem to be working
    #essentially, the first item in this new dict is the last thing put into the database
    sorted_dictionary = OrderedDict(sorted(myList.items(), key=lambda v: v, reverse=True))
    context = {
        'jerseys' : sorted_dictionary
    }
    return render(request,'web_app/index.html',context)

def jersey_by_size(request,size):
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
        'jerseys' : myList
    }
    return render(request,'web_app/index.html',context)


def item_detail(request,id):
    data = None
    template = None
    context = None
    with urllib.request.urlopen('http://exp:8000/exp/jersey_detail/'+str(id)) as response:
        data = response.read().decode('UTF-8')
    json_data = json.loads(data)
    if 'error' in json_data:
        template = '404.html'
    else:
        template = 'web_app/item_detail.html'
        context = {
            'jersey' : json_data[0]['fields']
        }
    return render(request,template,context)

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
                "email":email,
                "first_name":first_name,
                "last_name":last_name,
                "password":password,
                "shirt_size":shirt_size
            }

            data = urllib.parse.urlencode(register_data)
            
            data = urllib.parse.urlencode(register_data).encode("utf-8")
            req = urllib.request.Request('http://exp:8000/exp/users/register/')
            with urllib.request.urlopen(req,data=data) as f:
                resp = f.read()


            resp_text = resp.decode('utf-8')
            resp_dict = json.loads(resp_text)

            f = open("request.txt", "a")
            # f.write(req.data.decode('utf-8'))
            f.write(resp_text)
            f.close()


            if not resp or not resp_dict['ok']:
                #todo figure out how to display possible errors here
                return render(request, 'web_app/login.html', {'form' : form,'error' : resp_dict['error']})
            authenticator = resp_dict['resp']['authenticator'] #this is not going to work
            response = HttpResponseRedirect('index')
            response.set_cookie("auth", authenticator)
            return response
        else:
            return render(request, 'web_app/register.html', {'form' : form, })
    else:
        form = RegisterForm()
    return render(request, 'web_app/register.html', {'form' : form, 'get': True})
    # return HttpResponse("<h1> Hello World </h1>")

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            #cleaning the data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            login_data = {"email" : email, "password" : password}
            #our next page
            next = reverse('index')
            resp = urllib.request.Request('http://exp:8000/exp/users/login', data=login_data)
            resp_json = json.dumps(resp)
            if not resp or not resp_json['ok']:
                #todo figure out how to display possible errors here
                return render(request, 'web_app/login.html', {'form': form})

            # at this point we can log them in

            authenticator = resp_json['resp']['authenticator']
            response = HttpResponseRedirect(next)
            response.set_cookie("auth",authenticator)
            return response
        else:
            return render(request, 'web_app/login.html', {'form' : form})
    else:
        form = LoginForm()
    return render(request, 'web_app/login.html', { 'form' : form})
    # return HttpResponse("<h1> Hello World </h1>")
    