from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Item
from .forms import ItemForm


def item_list(request):
    itens = Item.objects.all().order_by('nome')
    return render(request, 'item/item_list.html', {'itens': itens})


def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item cadastrado com sucesso!')
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'item/item_form.html', {'form': form})