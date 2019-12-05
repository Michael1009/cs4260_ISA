from django.urls import path
from django.urls import include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Create
    path('api/v1/Jersey/create', views.create_jersey, name='create_jersey'),
    # Read
    path('api/v1/Jersey', views.get_all_jersey, name='get_jersey'),
    path('api/v1/User', views.get_all_user, name='get_user'),
    path('api/v1/Jersey/<int:id>', views.get_jersey, name='get_jersey'),
    path('api/v1/User/<int:id>', views.get_user, name='get_user'),
    path('api/v1/Jersey/<str:size>',
         views.get_jersey_by_size, name='get_jersey_by_size'),
    # Update
    path('api/v1/Jersey/<int:id>/update',
         views.update_jersey, name='update_jersey'),
    path('api/v1/User/<int:id>/update',
         views.update_user, name='update_user'),
    # Delete
    path('api/v1/User/<int:id>/delete', views.delete_user, name='delete_user'),
    path('api/v1/User/<str:email>/delete_user_by_email', views.delete_user_by_email, name='delete_user_by_email'),
    path('api/v1/Jersey/<int:id>/delete',views.delete_jersey, name='delete_jersey'),


    # Authenticate
    path('api/v1/users/register', views.register, name="register"),
    path('api/v1/users/login', views.login, name="login"),
    path('api/v1/users/logout', views.logout, name="logout"),
    path('api/v1/info', views.info, name="info"),
]
