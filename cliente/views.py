from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cliente
from .forms import ClienteForm


def cliente_list(request):
    clientes = Cliente.objects.all().order_by('username')
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})


def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'cliente/cliente_form.html', {'form': form})