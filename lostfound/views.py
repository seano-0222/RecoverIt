from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from lostfound.models import LostItem, FoundItem, Claim
from .decorators import admin_required


@admin_required
def index(request):
    context = {
        'total_users': User.objects.count(),
        'total_lost_items': LostItem.objects.count(),
        'total_found_items': FoundItem.objects.count(),
        'pending_claims': Claim.objects.filter(status='pending').count(),
    }
    return render(request, 'dashboard/index.html', context)


@admin_required
def users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/users.html', {'users': users})


@admin_required
def lost_items_view(request):
    items = LostItem.objects.all().order_by('-created_at')
    return render(request, 'dashboard/lost_items.html', {'items': items})


@admin_required
def found_items_view(request):
    items = FoundItem.objects.all().order_by('-created_at')
    return render(request, 'dashboard/found_items.html', {'items': items})


@admin_required
def claims_view(request):
    claims = Claim.objects.all().order_by('-created_at')
    return render(request, 'dashboard/claims.html', {'claims': claims})