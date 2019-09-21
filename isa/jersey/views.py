from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Jersey
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the jersey index.")

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        form = request.POST
        try:
            new_user = User(
                email=request.POST['email'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                shirt_size=request.POST['shirt_size']
            )
            new_user.save()
        except: 
            result = json.dumps(
                {'error': 'Missing field or malformed data in CREATE request. Here is the data we received: {}'.format(form), 'ok': False})
            return HttpResponse(result)

    return HttpResponse(status=201)

@csrf_exempt
def create_jersey(request):
    new_jersey = Jersey(
        team=request.POST['team'],
        number=request.POST['number'],
        player=request.POST['player'],
        shirt_size=request.POST['shirt_size'],
        primary_color=request.POST['primary_color'],
        secondary_color=request.POST['secondary_color']
    )
    new_jersey.save()

    return HttpResponse(status=201)
