from django.shortcuts import render
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
    form = RegisterForm()
    args = {'form': form}
    url = 'http://exp:8000/exp/users/create'
    return render(request, "register.html", args)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # here is where we would send the email and password down our tiers to verify it
            # for now just sending back to the homepage
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})
    