from django import forms
from django.contrib.auth.models import User
from .models import Cliente


class ClienteForm(forms.ModelForm):
    # 'password' fica FORA de Meta.fields de propósito: assim o ModelForm nunca
    # grava o texto digitado direto no campo (na edição, deixar em branco
    # apagaria a senha). Quem grava é o save(), com set_password().
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Cliente
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Editando: a senha só muda se a pessoa digitar uma nova.
            self.fields['password'].required = False
            self.fields['password'].label = 'Nova senha'
            self.fields['password'].help_text = 'Deixe em branco para manter a senha atual.'

    def clean_username(self):
        username = self.cleaned_data['username']
        outros = User.objects.filter(username=username)
        if self.instance.pk:
            outros = outros.exclude(pk=self.instance.pk)
        if outros.exists():
            raise forms.ValidationError('Já existe um usuário com esse nome. Escolha outro.')
        return username

    def save(self, commit=True):
        cliente = super().save(commit=False)
        senha = self.cleaned_data.get('password')
        if senha:
            cliente.set_password(senha)
        if commit:
            cliente.save()
        return cliente
