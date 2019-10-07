from django.shortcuts import render
from django.http import HttpResponse
import urllib.request, json

# Create your views here.

def index(request):
    data = None
    with urllib.request.urlopen('http://exp:8000/exp/home/') as response:
        data = response.read().decode('UTF-8')
    myList = []
    i = 0
    for fields in json.loads(data):
        bigData = json.loads(data)[i]['fields']
        i = i + 1
        myList.append(bigData)
    context = {
        'jerseys' : myList
    }
    return render(request,'web_app/index.html',context)

def item_detail(request,id):
    data = None
    template = None
    with urllib.request.urlopen('http://exp:8000/exp/jersey_detail/'+str(id)) as response:
        data = response.read().decode('UTF-8')
    context = {
        'jersey' : json.loads(data)[0]['fields']
    }
    template = 'web_app/item_detail.html'
    return render(request,template,context)