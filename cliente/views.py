from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao, manter_login_apos_trocar_senha
>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37
from .models import Cliente
from .forms import ClienteForm
from .grupo import garantir_grupo_cliente


def _adicionar_ao_grupo_cliente(usuario):
    """Garante que todo Cliente criado já entre no grupo 'Cliente' (com as permissões dele)."""
    garantir_grupo_cliente(usuario)


# Regra: a equipe usa as permissões do grupo; o cliente sempre pode ver, editar
# e excluir a PRÓPRIA conta (mesmo sem permissão de grupo).
def _e_o_proprio(usuario, cliente):
    return usuario.pk == cliente.pk


def pode_ver_cliente(usuario, cliente):
    return usuario.has_perm('cliente.view_cliente') or _e_o_proprio(usuario, cliente)


def pode_alterar_cliente(usuario, cliente):
    return usuario.has_perm('cliente.change_cliente') or _e_o_proprio(usuario, cliente)


def pode_excluir_cliente(usuario, cliente):
    return usuario.has_perm('cliente.delete_cliente') or _e_o_proprio(usuario, cliente)
>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37


@login_required
@permission_required('cliente.view_cliente', raise_exception=True)
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('username')
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})


@login_required
@permission_required('cliente.add_cliente', raise_exception=True)
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            _adicionar_ao_grupo_cliente(cliente)
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente/cliente_form.html', {'form': form})


def cadastro(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            _adicionar_ao_grupo_cliente(cliente)
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = ClienteForm()
    return render(request, 'cliente/cadastro.html', {'form': form})


@login_required
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if not pode_ver_cliente(request.user, cliente):
        raise PermissionDenied
    return render(request, 'cliente/cliente_detail.html', {
        'cliente': cliente,
        'pode_editar': pode_alterar_cliente(request.user, cliente),
        'pode_excluir': pode_excluir_cliente(request.user, cliente),
        'eh_proprio': _e_o_proprio(request.user, cliente),
    })


@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if not pode_alterar_cliente(request.user, cliente):
        raise PermissionDenied
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            if form.cleaned_data.get('password'):
                manter_login_apos_trocar_senha(request, cliente.pk)
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/cliente_form.html', {'form': form, 'cliente': cliente})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if not pode_excluir_cliente(request.user, cliente):
        raise PermissionDenied
    proprio = _e_o_proprio(request.user, cliente)
    return confirmar_exclusao(
        request, cliente,
        titulo='Excluir minha conta' if proprio else 'Excluir cliente',
        aviso='Clientes que já fizeram pedidos não podem ser excluídos (o histórico é mantido).',
        cancelar_url=reverse('cliente_detail', args=[cliente.pk]),
        sucesso_url=reverse('login') if proprio else reverse('cliente_list'),
        sucesso_msg='Conta excluída com sucesso.' if proprio else 'Cliente excluído com sucesso!',
        bloqueio_msg='Não é possível excluir: esse cliente já tem pedidos registrados.',
    )
