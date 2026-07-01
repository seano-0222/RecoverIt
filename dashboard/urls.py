from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_view, name='users'),
    path('lost-items/', views.lost_items_view, name='lost_items'),
    path('found-items/', views.found_items_view, name='found_items'),
    path('claims/', views.claims_view, name='claims'),
]