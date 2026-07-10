from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm


@login_required
def home(request):
    items = Item.objects.all().order_by('-created_at')

    item_type = request.GET.get('type')
    if item_type in ('lost', 'found'):
        items = items.filter(type=item_type)

    query = request.GET.get('q')
    if query:
        items = items.filter(item_name__icontains=query)

    return render(request, 'lostfound/home.html', {'items': items})


@login_required
def report_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Item reported successfully.')
            return redirect('lostfound:home')
    else:
        form = ItemForm()

    return render(request, 'lostfound/report_item.html', {'form': form})


@login_required
def my_items(request):
    items = Item.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'lostfound/my_items.html', {'items': items})