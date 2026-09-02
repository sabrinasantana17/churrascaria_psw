from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pedido
from .forms import PedidoForm


def pedido_list(request):
    pedidos = Pedido.objects.all().order_by('-criado_em')
    return render(request, 'pedido/pedido_list.html', {'pedidos': pedidos})


def pedido_create(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido criado com sucesso!')
            return redirect('pedido_list')
    else:
        form = PedidoForm()
    return render(request, 'pedido/pedido_form.html', {'form': form})