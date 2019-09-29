from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('jersey_detail/', views.jersey_detail, name='jersey_detail'),

]
