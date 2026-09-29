from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from pedido.acesso import pode_montar_pedido
from .models import Item
from .forms import ItemForm

@login_required
@permission_required('item.view_item', raise_exception=True)
def item_list(request):
    itens = Item.objects.all().order_by('nome')
    return render(request, 'item/item_list.html', {
        'itens': itens,
        'pode_montar_pedido': pode_montar_pedido(request.user),
    })


@login_required
@permission_required('item.add_item', raise_exception=True)
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


@login_required
@permission_required('item.view_item', raise_exception=True)
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item/item_detail.html', {'item': item})
