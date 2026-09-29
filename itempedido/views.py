from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao
from cliente.models import Cliente
from item.models import Item
from pedido.acesso import (
    pode_montar_pedido, e_dono_do_pedido,
    pode_alterar_item_pedido, pode_excluir_item_pedido,
)
from pedido.models import Pedido
from .models import ItemPedido
from .forms import ItemPedidoForm, ItemPedidoEditForm, AdicionarItemForm
from cliente.models import Cliente
from item.models import Item
from pedido.acesso import pode_montar_pedido
from pedido.models import Pedido
from .models import ItemPedido
from .forms import ItemPedidoForm, AdicionarItemForm
>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37

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


def _negar(request, item_pedido):
    """Cliente dono de pedido já enviado leva uma mensagem; os demais, 403."""
    if item_pedido.pedido.concluido and e_dono_do_pedido(request.user, item_pedido.pedido):
def _negar(request, item_pedido):
    """Cliente dono de pedido já enviado leva uma mensagem; os demais, 403."""
    if item_pedido.pedido.concluido and e_dono_do_pedido(request.user, item_pedido.pedido):
        messages.error(request, 'Esse pedido já foi enviado e não pode mais ser alterado.')
        return redirect('pedido_detail', pk=item_pedido.pedido_id)
    raise PermissionDenied


@login_required
def itempedido_update(request, pk):
    item_pedido = get_object_or_404(ItemPedido.objects.select_related('pedido', 'item'), pk=pk)
    if not pode_alterar_item_pedido(request.user, item_pedido):
        return _negar(request, item_pedido)
    if request.method == 'POST':
        form = ItemPedidoEditForm(request.POST, instance=item_pedido)
        if form.is_valid():
            form.save()
            messages.success(request, f'{item_pedido.item.nome} atualizado no pedido #{item_pedido.pedido_id}!')
            return redirect('pedido_detail', pk=item_pedido.pedido_id)
    else:
        form = ItemPedidoEditForm(instance=item_pedido)
    return render(request, 'itempedido/itempedido_form.html', {'form': form, 'item_pedido': item_pedido})


@login_required
def itempedido_delete(request, pk):
    item_pedido = get_object_or_404(ItemPedido.objects.select_related('pedido', 'item'), pk=pk)
    if not pode_excluir_item_pedido(request.user, item_pedido):
        return _negar(request, item_pedido)
    pedido_url = reverse('pedido_detail', args=[item_pedido.pedido_id])
    return confirmar_exclusao(
        request, item_pedido,
        titulo='Remover item do pedido',
        aviso=f'O total do pedido #{item_pedido.pedido_id} será recalculado.',
        cancelar_url=pedido_url,
        sucesso_url=pedido_url,
        sucesso_msg='Item removido do pedido!',
        bloqueio_msg='Não foi possível remover esse item.',
    )


>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37
def _pedido_atual(cliente):
    """Pedido que o cliente ainda está montando (não concluído), se existir."""
    return Pedido.objects.filter(cliente=cliente, concluido=False).order_by('-criado_em').first()


def _cliente_da_sessao(request):
    """Último cliente atendido por este funcionário (só para já vir selecionado)."""
    cliente_id = request.session.get('cliente_atendido')
    return Cliente.objects.filter(pk=cliente_id).first() if cliente_id else None


@login_required
def adicionar_item(request, item_pk):
    """Tela 'Itens do pedido'. O cliente monta o próprio pedido; funcionários e
    administradores escolhem o cliente do pedido. Ao salvar, o item entra no
    pedido em andamento desse cliente (criado automaticamente se não existir)."""
    cliente_logado = getattr(request.user, 'cliente', None)
    funcionario_logado = getattr(request.user, 'funcionario', None)
    eh_cliente = cliente_logado is not None

    if not pode_montar_pedido(request.user):
        messages.error(request, 'Você não tem permissão para montar pedidos.')
        return redirect('item_list')

    item = get_object_or_404(Item, pk=item_pk, disponivel=True)

    if request.method == 'POST':
        form = AdicionarItemForm(request.POST, mostrar_cliente=not eh_cliente)
        if form.is_valid():
            cliente = cliente_logado or form.cleaned_data['cliente']
            quantidade = form.cleaned_data['quantidade']
            observacao = form.cleaned_data['observacao']

            pedido = _pedido_atual(cliente)
            if pedido is None:
                pedido = Pedido.objects.create(cliente=cliente, funcionario=funcionario_logado)
            elif funcionario_logado is not None and pedido.funcionario_id is None:
                pedido.funcionario = funcionario_logado
                pedido.save(update_fields=['funcionario'])

            item_pedido, criado = ItemPedido.objects.get_or_create(
                pedido=pedido,
                item=item,
                defaults={
                    'quantidade': quantidade,
                    'observacao': observacao,
                    'preco_conjunto': item.preco * quantidade,
                },
            )
            if not criado:
                # O item já estava no pedido: soma a quantidade.
                item_pedido.quantidade += quantidade
                if observacao:
                    if item_pedido.observacao:
                        observacao = f'{item_pedido.observacao}; {observacao}'
                    item_pedido.observacao = observacao[:200]
                item_pedido.preco_conjunto = item.preco * item_pedido.quantidade
                item_pedido.save()

            if not eh_cliente:
                request.session['cliente_atendido'] = cliente.pk

            messages.success(request, f'{item.nome} adicionado ao pedido #{pedido.pk}!')
            return redirect('pedido_detail', pk=pedido.pk)
        cliente_ref = cliente_logado or _cliente_da_sessao(request)
    else:
        cliente_ref = cliente_logado or _cliente_da_sessao(request)
        initial = {'quantidade': 1}
        if not eh_cliente and cliente_ref is not None:
            initial['cliente'] = cliente_ref.pk
        form = AdicionarItemForm(initial=initial, mostrar_cliente=not eh_cliente)

    pedido = _pedido_atual(cliente_ref) if cliente_ref is not None else None
    itens_do_pedido = pedido.itempedido_set.select_related('item') if pedido else []
    return render(request, 'itempedido/adicionar_item.html', {
        'form': form,
        'item': item,
        'pedido': pedido,
        'itens_do_pedido': itens_do_pedido,
    })
