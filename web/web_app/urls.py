from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('item/<int:id>', views.item_detail, name='item_detail')
]