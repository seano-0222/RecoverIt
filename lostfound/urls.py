from django.urls import path
from . import views

app_name = 'lostfound'

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'),
    path('my-items/', views.my_items, name='my_items'),
]