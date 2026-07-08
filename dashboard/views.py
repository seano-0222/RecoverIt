from django.shortcuts import render
from django.contrib.auth.models import User
from lostfound.models import Item
from .decorators import admin_required


@admin_required
def index(request):
    context = {
        'total_users': User.objects.count(),
        'total_items': Item.objects.count(),
        'total_lost_items': Item.objects.filter(type='lost').count(),
        'total_found_items': Item.objects.filter(type='found').count(),
    }
    return render(request, 'dashboard/index.html', context)


@admin_required
def users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})


@admin_required
def items_view(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'dashboard/items.html', {'items': items})