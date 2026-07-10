from django.urls import path
from . import views

app_name = 'lostfound'

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'),
    path('my-items/', views.my_items, name='my_items'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/chat/', views.item_chat, name='item_chat'),
    path('item/<int:pk>/chat/<int:user_id>/', views.item_chat, name='item_chat_with'),
    path('item/<int:pk>/mark-found/<int:user_id>/', views.item_mark_found, name='item_mark_found'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
]