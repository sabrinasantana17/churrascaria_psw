from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Pedido
from .forms import PedidoForm

@login_required
@permission_required('pedido.view_pedido', raise_exception=True)
def pedido_list(request):
    # Cliente só pode ver os próprios pedidos (regra de negócio, não dá
    # pra expressar isso só com a permission de model, então filtra aqui).
    if hasattr(request.user, 'cliente'):
        pedidos = Pedido.objects.filter(cliente=request.user.cliente).order_by('-criado_em')
    else:
        pedidos = Pedido.objects.all().order_by('-criado_em')
    return render(request, 'pedido/pedido_list.html', {'pedidos': pedidos})

@login_required
@permission_required('pedido.add_pedido', raise_exception=True)
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

@login_required
@permission_required('pedido.view_pedido', raise_exception=True)
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    # Mesma regra da listagem: cliente só pode ver o detalhe dos próprios pedidos.
    if hasattr(request.user, 'cliente') and pedido.cliente_id != request.user.cliente.id:
        messages.error(request, 'Você não tem permissão para ver esse pedido.')
        return redirect('pedido_list')
    itens_do_pedido = pedido.itempedido_set.select_related('item').all()
    return render(request, 'pedido/pedido_detail.html', {'pedido': pedido, 'itens_do_pedido': itens_do_pedido})