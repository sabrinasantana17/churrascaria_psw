from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from churrascaria.utils import confirmar_exclusao
from .models import Feedback
from .forms import FeedbackForm, FeedbackRespostaForm


# Regras:
# - editar o TEXTO: só quem enviou, e só enquanto não foi respondido;
# - marcar como respondido: equipe com permissão de alterar feedbacks
#   (que não seja o próprio autor);
# - excluir: quem enviou, ou equipe com permissão de excluir feedbacks.
def _e_autor(usuario, feedback):
    return feedback.usuario_id == usuario.pk


def pode_editar_texto(usuario, feedback):
    return _e_autor(usuario, feedback) and not feedback.respondido


def pode_responder(usuario, feedback):
    return usuario.has_perm('feedback.change_feedback') and not _e_autor(usuario, feedback)


def pode_excluir(usuario, feedback):
    return _e_autor(usuario, feedback) or usuario.has_perm('feedback.delete_feedback')


def _pode_ver(usuario, feedback):
    return _e_autor(usuario, feedback) or usuario.has_perm('feedback.view_feedback')


@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.usuario = request.user
            feedback.save()
            messages.success(request, 'Obrigado! Seu feedback foi enviado com sucesso.')
            return redirect('feedback_list')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form, 'modo': 'novo'})


@login_required
def feedback_list(request):
    # Quem tem a permissão de ver feedbacks (gerência) enxerga todos;
    # o usuário comum vê apenas os feedbacks que ele mesmo enviou.
    if request.user.has_perm('feedback.view_feedback'):
        feedbacks = Feedback.objects.all()
        todos = True
    else:
        feedbacks = Feedback.objects.filter(usuario=request.user)
        todos = False
    feedbacks = list(feedbacks.select_related('usuario'))
    for feedback in feedbacks:
        feedback.pode_alterar = (pode_editar_texto(request.user, feedback)
                                 or pode_responder(request.user, feedback))
        feedback.pode_excluir = pode_excluir(request.user, feedback)
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks, 'todos': todos})


@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    # Só pode ver o detalhe quem enviou o feedback ou quem tem a permissão de ver todos.
    if not _pode_ver(request.user, feedback):
        raise PermissionDenied
    return render(request, 'feedback/feedback_detail.html', {
        'feedback': feedback,
        'pode_editar': pode_editar_texto(request.user, feedback),
        'pode_responder': pode_responder(request.user, feedback),
        'pode_excluir': pode_excluir(request.user, feedback),
    })


@login_required
def feedback_update(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if pode_editar_texto(request.user, feedback):
        form_class, modo = FeedbackForm, 'editar'
    elif pode_responder(request.user, feedback):
        form_class, modo = FeedbackRespostaForm, 'responder'
    elif _e_autor(request.user, feedback):
        messages.error(request, 'Esse feedback já foi respondido e não pode mais ser editado.')
        return redirect('feedback_detail', pk=feedback.pk)
    else:
        raise PermissionDenied

    if request.method == 'POST':
        form = form_class(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback atualizado com sucesso!')
            return redirect('feedback_detail', pk=feedback.pk)
    else:
        form = form_class(instance=feedback)
    return render(request, 'feedback/feedback_form.html', {
        'form': form, 'modo': modo, 'feedback': feedback,
    })


@login_required
def feedback_delete(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    if not pode_excluir(request.user, feedback):
        raise PermissionDenied
    return confirmar_exclusao(
        request, feedback,
        titulo='Excluir feedback',
        cancelar_url=reverse('feedback_detail', args=[feedback.pk]),
        sucesso_url=reverse('feedback_list'),
        sucesso_msg='Feedback excluído com sucesso!',
        bloqueio_msg='Não foi possível excluir esse feedback.',
    )
