from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from .models import Cliente
from .forms import ClienteForm


def _adicionar_ao_grupo_cliente(usuario):
    """Garante que todo Cliente criado já entre no grupo 'Cliente'."""
    grupo, _ = Group.objects.get_or_create(name='Cliente')
    usuario.groups.add(grupo)


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
@permission_required('cliente.view_cliente', raise_exception=True)
def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'cliente/cliente_detail.html', {'cliente': cliente})