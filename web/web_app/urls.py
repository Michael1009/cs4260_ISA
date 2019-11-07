from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('item/<int:id>', views.item_detail, name='item_detail'),
     path('jersey/trending', views.jersey_trending, name='jersey_trending'),
     path('jersey/<str:size>', views.jersey_by_size, name='jersey_detail'),
     path('register', views.register, name="register"),
     path('login_page', views.login, name="login_page"),
     path('logout', views.logout, name="logout"),
     path('create_jersey', views.create_jersey, name ='create_jersey'),
     path('search', views.search, name = "search"),
]