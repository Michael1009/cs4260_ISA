from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/Jersey/create', views.create_jersey, name='create_jersey'),
    path('api/v1/User/create', views.create_user, name='create_user')
]
