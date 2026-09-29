from django import forms
from django.contrib.auth.models import User
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    # 'password' fica FORA de Meta.fields de propósito (ver ClienteForm): na
    # edição, deixar em branco não pode apagar a senha atual.
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Funcionario
        fields = ['username', 'first_name', 'last_name', 'email', 'cargo', 'telefone', 'salario']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'cargo': 'Cargo',
            'telefone': 'Telefone',
            'salario': 'Salário',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
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
        funcionario = super().save(commit=False)
        senha = self.cleaned_data.get('password')
        if senha:
            funcionario.set_password(senha)
        if commit:
            funcionario.save()
        return funcionario
