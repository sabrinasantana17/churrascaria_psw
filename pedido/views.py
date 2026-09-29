from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
<<<<<<< HEAD
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao
from .acesso import (
    pode_montar_pedido, e_dono_do_pedido, pode_alterar_pedido, pode_excluir_pedido,
    pode_alterar_item_pedido, pode_excluir_item_pedido,
)
from .forms import PedidoEditForm
=======
from .acesso import pode_montar_pedido
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
from .models import Pedido

@login_required
@permission_required('pedido.view_pedido', raise_exception=True)
def pedido_list(request):
    eh_cliente = hasattr(request.user, 'cliente')
    if eh_cliente:
        # Cliente só vê os próprios pedidos (inclusive o que ainda está montando).
        pedidos = Pedido.objects.filter(cliente=request.user.cliente).order_by('-criado_em')
    else:
        # Equipe/administradores veem todos os pedidos, do mais recente para o
        # mais antigo (a coluna Status mostra se está em andamento ou enviado).
        pedidos = Pedido.objects.all().order_by('-criado_em')
<<<<<<< HEAD
    pedidos = list(pedidos.select_related('cliente', 'funcionario'))
    for pedido in pedidos:
        pedido.pode_alterar = pode_alterar_pedido(request.user, pedido)
        pedido.pode_excluir = pode_excluir_pedido(request.user, pedido)
=======
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
    return render(request, 'pedido/pedido_list.html', {
        'pedidos': pedidos,
        'eh_cliente': eh_cliente,
        'pode_montar': pode_montar_pedido(request.user),
    })

@login_required
def pedido_create(request):
    # Ninguém preenche formulário de pedido: o pedido é criado automaticamente
    # quando o primeiro item é adicionado pelo cardápio ("Itens do pedido").
    messages.info(request, 'Escolha os itens do cardápio para montar o pedido.')
    return redirect('item_list')

@login_required
@permission_required('pedido.view_pedido', raise_exception=True)
def pedido_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    eh_cliente = hasattr(request.user, 'cliente')
    # Mesma regra da listagem: cliente só pode ver o detalhe dos próprios pedidos.
    if eh_cliente and pedido.cliente_id != request.user.cliente.id:
        messages.error(request, 'Você não tem permissão para ver esse pedido.')
        return redirect('pedido_list')
<<<<<<< HEAD
    itens_do_pedido = list(pedido.itempedido_set.select_related('item', 'pedido').all())
    for ip in itens_do_pedido:
        ip.pode_alterar = pode_alterar_item_pedido(request.user, ip)
        ip.pode_excluir = pode_excluir_item_pedido(request.user, ip)
=======
    itens_do_pedido = pedido.itempedido_set.select_related('item').all()
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
    return render(request, 'pedido/pedido_detail.html', {
        'pedido': pedido,
        'itens_do_pedido': itens_do_pedido,
        'eh_cliente': eh_cliente,
        'pode_montar': pode_montar_pedido(request.user),
<<<<<<< HEAD
        'pode_alterar': pode_alterar_pedido(request.user, pedido),
        'pode_excluir': pode_excluir_pedido(request.user, pedido),
        'mostrar_acoes_itens': any(ip.pode_alterar or ip.pode_excluir for ip in itens_do_pedido),
    })


@login_required
def pedido_update(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if not pode_alterar_pedido(request.user, pedido):
        raise PermissionDenied
    if request.method == 'POST':
        form = PedidoEditForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pedido #{pedido.pk} atualizado com sucesso!')
            return redirect('pedido_detail', pk=pedido.pk)
    else:
        form = PedidoEditForm(instance=pedido)
    return render(request, 'pedido/pedido_form.html', {'form': form, 'pedido': pedido})


@login_required
def pedido_delete(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if not pode_excluir_pedido(request.user, pedido):
        if pedido.concluido and e_dono_do_pedido(request.user, pedido):
            messages.error(request, 'Pedidos já enviados não podem ser cancelados por aqui. Fale com a equipe.')
            return redirect('pedido_detail', pk=pedido.pk)
        raise PermissionDenied
    eh_cliente = hasattr(request.user, 'cliente')
    return confirmar_exclusao(
        request, pedido,
        titulo='Cancelar pedido' if eh_cliente else 'Excluir pedido',
        aviso='Todos os itens lançados nesse pedido também serão apagados.',
        cancelar_url=reverse('pedido_detail', args=[pedido.pk]),
        sucesso_url=reverse('pedido_list'),
        sucesso_msg='Pedido excluído com sucesso!',
        bloqueio_msg='Não foi possível excluir esse pedido.',
    )

=======
    })

>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
@login_required
def concluir_pedido(request, pk):
    """Confirma o pedido: a partir daqui ele foi enviado e não recebe mais itens.
    O cliente conclui os próprios pedidos; funcionários/administradores concluem
    qualquer pedido (desde que possam montar pedidos)."""
    cliente = getattr(request.user, 'cliente', None)
    if cliente is not None:
        pedido = get_object_or_404(Pedido, pk=pk, cliente=cliente)
    elif pode_montar_pedido(request.user):
        pedido = get_object_or_404(Pedido, pk=pk)
    else:
        messages.error(request, 'Você não tem permissão para concluir pedidos.')
        return redirect('pedido_list')

    if request.method != 'POST':
        return redirect('pedido_detail', pk=pedido.pk)

    if pedido.concluido:
        messages.info(request, f'O pedido #{pedido.pk} já foi enviado.')
    elif not pedido.itempedido_set.exists():
        messages.error(request, 'Adicione pelo menos um item antes de concluir o pedido.')
    else:
        pedido.concluido = True
        funcionario = getattr(request.user, 'funcionario', None)
        if funcionario is not None and pedido.funcionario_id is None:
            pedido.funcionario = funcionario
        pedido.save()
        messages.success(request, f'Pedido #{pedido.pk} enviado com sucesso!')
    return redirect('pedido_detail', pk=pedido.pk)
