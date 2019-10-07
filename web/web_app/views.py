from django.shortcuts import render
from django.http import HttpResponse
import urllib.request, json

# Create your views here.

def index(request):
    return render(request,'web_app/index.html')

def item_detail(request,id):
    data = None
    code = None
    template = None
    with urllib.request.urlopen('http://exp:8000/exp/jersey_detail/'+str(id)) as response:
        data = response.read().decode('UTF-8')
        code = response.getcode()
    if code == 404:
        template = 'web_app/404.html'
    elif code == 200:
        context = {
            'jersey' : json.loads(data)[0]['fields']
        }
        template = 'web_app/item_detail.html'
    return render(request,template,context)