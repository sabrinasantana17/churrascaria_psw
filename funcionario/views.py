from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Funcionario
from .forms import FuncionarioForm
from .grupo import garantir_grupo_funcionario


def _adicionar_ao_grupo_cargo(funcionario):
    """Garante que todo Funcionario criado entre no grupo do seu cargo
    (Gerente, Garçom ou Cozinheiro), com as permissões básicas."""
    garantir_grupo_funcionario(funcionario)


@login_required
@permission_required('funcionario.view_funcionario', raise_exception=True)
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('username')
    return render(request, 'funcionario/funcionario_list.html', {'funcionarios': funcionarios})


@login_required
@permission_required('funcionario.add_funcionario', raise_exception=True)
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            funcionario = form.save()
            _adicionar_ao_grupo_cargo(funcionario)
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('funcionario_list')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionario/funcionario_form.html', {'form': form})


@login_required
@permission_required('funcionario.view_funcionario', raise_exception=True)
def funcionario_detail(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, 'funcionario/funcionario_detail.html', {'funcionario': funcionario})