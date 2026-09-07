from django.shortcuts import render, redirect
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