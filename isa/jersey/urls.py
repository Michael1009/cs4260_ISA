from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/Jersey/create', views.create_jersey, name='create_jersey'),
    path('api/v1/Jersey/<int:id>/update',
         views.update_jersey, name='update_jersey'),
    path('api/v1/User/create', views.create_user, name='create_user'),
    path('api/v1/User/<int:id>/update',
         views.update_user, name='update_user'),
    path('api/v1/User/<int:id>/delete', views.delete_user, name='delete_user')
]
