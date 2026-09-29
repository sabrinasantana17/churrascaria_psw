from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao
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


@login_required
@permission_required('item.change_item', raise_exception=True)
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item atualizado com sucesso!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'item/item_form.html', {'form': form, 'item': item})


@login_required
@permission_required('item.delete_item', raise_exception=True)
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return confirmar_exclusao(
        request, item,
        titulo='Excluir item do cardápio',
        aviso='Se o item já foi vendido, em vez de excluir, edite-o e desmarque "Disponível".',
        cancelar_url=reverse('item_detail', args=[item.pk]),
        sucesso_url=reverse('item_list'),
        sucesso_msg='Item excluído com sucesso!',
        bloqueio_msg='Esse item já aparece em pedidos e não pode ser excluído. '
                     'Edite-o e desmarque "Disponível" para tirá-lo do cardápio.',
    )
