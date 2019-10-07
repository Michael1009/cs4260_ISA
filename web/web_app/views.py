from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request,'web_app/index.html')

def item_detail(request,id):
    return render(request,'web_app/item_detail.html')