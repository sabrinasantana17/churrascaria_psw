from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.shortcuts import redirect, render


def manter_login_apos_trocar_senha(request, usuario_pk):
    """Trocar a senha invalida a sessão. Se a pessoa trocou a PRÓPRIA senha,
    renovamos a sessão para ela não ser deslogada no meio da edição."""
    if request.user.pk == usuario_pk:
        update_session_auth_hash(request, User.objects.get(pk=usuario_pk))


def confirmar_exclusao(request, objeto, *, titulo, aviso='', cancelar_url,
                       sucesso_url, sucesso_msg, bloqueio_msg):
    """Tela de confirmação + exclusão de qualquer objeto.

    GET  -> mostra "tem certeza?".
    POST -> exclui. Se o banco protege o registro (ex.: item que já está em
            pedidos), mostra `bloqueio_msg` e nada é apagado.
    As URLs precisam vir prontas (calculadas antes da exclusão)."""
    if request.method == 'POST':
        try:
            objeto.delete()
        except ProtectedError:
            messages.error(request, bloqueio_msg)
            return redirect(cancelar_url)
        messages.success(request, sucesso_msg)
        return redirect(sucesso_url)
    return render(request, 'confirmar_exclusao.html', {
        'objeto': objeto,
        'titulo': titulo,
        'aviso': aviso,
        'cancelar_url': cancelar_url,
    })
