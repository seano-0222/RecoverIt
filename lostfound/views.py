from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Item, Message
from .forms import ItemForm, MessageForm


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

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_owner = item.user == request.user

    threads = None
    if is_owner:
        partner_ids = Message.objects.filter(item=item).exclude(sender=request.user).values_list('sender', flat=True).distinct()
        threads = User.objects.filter(id__in=partner_ids)

    return render(request, 'lostfound/item_detail.html', {
        'item': item,
        'is_owner': is_owner,
        'threads': threads,
    })


@login_required
def item_chat(request, pk, user_id=None):
    item = get_object_or_404(Item, pk=pk)

    if request.user == item.user:
        if user_id is None:
            messages.error(request, "Select a conversation to view.")
            return redirect('lostfound:item_detail', pk=item.pk)
        partner = get_object_or_404(User, pk=user_id)
    else:
        partner = item.user

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.item = item
            msg.sender = request.user
            msg.receiver = partner
            msg.save()
            if user_id is not None:
                return redirect('lostfound:item_chat_with', pk=item.pk, user_id=partner.pk)
            return redirect('lostfound:item_chat', pk=item.pk)
    else:
        form = MessageForm()

    thread = Message.objects.filter(item=item).filter(
        (Q(sender=request.user) & Q(receiver=partner)) | (Q(sender=partner) & Q(receiver=request.user))
    )

    return render(request, 'lostfound/item_chat.html', {
        'item': item,
        'partner': partner,
        'thread': thread,
        'form': form,
    })


@login_required
def item_mark_found(request, pk, user_id):
    item = get_object_or_404(Item, pk=pk)
    if item.user != request.user:
        messages.error(request, "Only the reporter can update this item.")
        return redirect('lostfound:item_detail', pk=item.pk)

    finder = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        item.status = 'resolved'
        item.found_by = finder
        item.save()
        messages.success(request, f"Item marked as found by {finder.username}.")
    return redirect('lostfound:item_detail', pk=item.pk)


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user != request.user:
        messages.error(request, "Only the reporter can delete this item.")
        return redirect('lostfound:item_detail', pk=item.pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item report deleted.")
        return redirect('lostfound:home')
    return redirect('lostfound:item_detail', pk=item.pk)

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user != request.user:
        messages.error(request, "Only the reporter can edit this item.")
        return redirect('lostfound:item_detail', pk=item.pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect('lostfound:item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'lostfound/item_edit.html', {'form': form, 'item': item})