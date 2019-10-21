from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('item/<int:id>', views.item_detail, name='item_detail'),
     path('jersey/<str:size>', views.jersey_by_size, name='jersey_detail'),
     path('register', views.register, name="register"),
     path('login_page', views.login, name="login_page"),
     path('logout', views.logout, name="logout"),
]