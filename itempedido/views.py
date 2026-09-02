from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ItemPedido
from .forms import ItemPedidoForm


def itempedido_list(request):
    itens_pedido = ItemPedido.objects.all().order_by('pedido_id')
    return render(request, 'itempedido/itempedido_list.html', {'itens_pedido': itens_pedido})


def itempedido_create(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item do pedido cadastrado com sucesso!')
            return redirect('itempedido_list')
    else:
        form = ItemPedidoForm()
    return render(request, 'itempedido/itempedido_form.html', {'form': form})
