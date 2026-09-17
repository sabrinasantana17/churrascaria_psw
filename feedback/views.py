from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Feedback
from .forms import FeedbackForm


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
    return render(request, 'feedback/feedback_form.html', {'form': form})


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
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks, 'todos': todos})


@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    # Só pode ver o detalhe quem enviou o feedback ou quem tem a permissão de ver todos.
    if feedback.usuario != request.user and not request.user.has_perm('feedback.view_feedback'):
        raise PermissionDenied
    return render(request, 'feedback/feedback_detail.html', {'feedback': feedback})