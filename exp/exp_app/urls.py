from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/<str:size>', views.jersey_by_size, name='jersey_by_size'),
    path('jersey_detail/<int:id>', views.jersey_detail_noauth, name='jersey_detail_noauth'),
    path('jersey_detail/<int:id>/<str:user_id>', views.jersey_detail, name='jersey_detail'),
    path('recommendation/<int:id>', views.get_recommendation, name='get_recommendation'),

    # Register
    path('users/register/', views.register),
    path('users/login/', views.login),
    path('users/create_item/', views.create_item),

    # get user info
    path('info/', views.info),
    
    # ES
    path('search/', views.search),
    path('trending/', views.trending),

]
