from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['tipo', 'mensagem']
        labels = {
            'tipo': 'Tipo de feedback',
            'mensagem': 'Sua mensagem',
        }
        widgets = {
            'mensagem': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': 'Conte pra gente o que você achou do sistema, o que poderia melhorar...',
                }
            ),
        }

    def clean_mensagem(self):
        mensagem = self.cleaned_data['mensagem'].strip()
        if len(mensagem) < 10:
            raise forms.ValidationError('Escreva um pouco mais para a gente entender melhor (mínimo 10 caracteres).')
        return mensagem


class FeedbackRespostaForm(forms.ModelForm):
    """Usado pela equipe (quem tem permissão de alterar feedbacks) só para
    marcar se o feedback já foi respondido. A mensagem é de quem enviou."""

    class Meta:
        model = Feedback
        fields = ['respondido']
        labels = {'respondido': 'Já foi respondido'}
