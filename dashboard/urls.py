from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_view, name='users'),
    path('items/', views.items_view, name='items'),
    path('items/<int:pk>/delete/', views.item_admin_delete, name='item_admin_delete'),
]