from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao, manter_login_apos_trocar_senha
from .models import Funcionario
from .forms import FuncionarioForm
from .grupo import garantir_grupo_funcionario, atualizar_grupo_funcionario


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
    return render(request, 'funcionario/funcionario_detail.html', {
        'funcionario': funcionario,
        'eh_proprio': funcionario.pk == request.user.pk,
    })


@login_required
@permission_required('funcionario.change_funcionario', raise_exception=True)
def funcionario_update(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            funcionario = form.save()
            atualizar_grupo_funcionario(funcionario)  # cargo pode ter mudado
            if form.cleaned_data.get('password'):
                manter_login_apos_trocar_senha(request, funcionario.pk)
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('funcionario_detail', pk=funcionario.pk)
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'funcionario/funcionario_form.html', {
        'form': form,
        'funcionario': funcionario,
    })


@login_required
@permission_required('funcionario.delete_funcionario', raise_exception=True)
def funcionario_delete(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if funcionario.pk == request.user.pk:
        messages.error(request, 'Você não pode excluir a sua própria conta de funcionário.')
        return redirect('funcionario_detail', pk=funcionario.pk)
    return confirmar_exclusao(
        request, funcionario,
        titulo='Excluir funcionário',
        aviso='Os pedidos atendidos por ele continuam no sistema, apenas sem funcionário associado. '
              'Os feedbacks enviados por ele também são apagados.',
        cancelar_url=reverse('funcionario_detail', args=[funcionario.pk]),
        sucesso_url=reverse('funcionario_list'),
        sucesso_msg='Funcionário excluído com sucesso!',
        bloqueio_msg='Não foi possível excluir esse funcionário.',
    )
