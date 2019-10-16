from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/<str:size>', views.jersey_by_size, name='jersey_by_size'),
    path('jersey_detail/<int:id>', views.jersey_detail, name='jersey_detail'),
 
    # Register
    path('users/create', views.register)

]
