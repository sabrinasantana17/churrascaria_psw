from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import ItemPedido
from .forms import ItemPedidoForm

@login_required
@permission_required('itempedido.view_itempedido', raise_exception=True)
def itempedido_list(request):
    itens_pedido = ItemPedido.objects.all().order_by('pedido_id')
    return render(request, 'itempedido/itempedido_list.html', {'itens_pedido': itens_pedido})

@login_required
@permission_required('itempedido.add_itempedido', raise_exception=True)
def itempedido_create(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item do pedido cadastrado com sucesso!')
            return redirect('itempedido_list')
    else:
        form = ItemPedidoForm(user=request.user)
    return render(request, 'itempedido/itempedido_form.html', {'form': form})

@login_required
@permission_required('itempedido.view_itempedido', raise_exception=True)
def itempedido_detail(request, pk):
    item_pedido = get_object_or_404(ItemPedido, pk=pk)
    return render(request, 'itempedido/itempedido_detail.html', {'item_pedido': item_pedido})