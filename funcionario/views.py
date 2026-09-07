from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Funcionario
from .forms import FuncionarioForm

@login_required
def funcionario_list(request):
    funcionarios = Funcionario.objects.all().order_by('username')
    return render(request, 'funcionario/funcionario_list.html', {'funcionarios': funcionarios})

@login_required
def funcionario_create(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('funcionario_list')
    else:
        form = FuncionarioForm()
    return render(request, 'funcionario/funcionario_form.html', {'form': form})