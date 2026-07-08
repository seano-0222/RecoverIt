from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_view, name='users'),
    path('items/', views.items_view, name='items'),
]