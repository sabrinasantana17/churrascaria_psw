from django import forms
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Funcionario
        fields = ['username', 'first_name', 'last_name', 'email', 'cargo', 'telefone', 'salario', 'password']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'cargo': 'Cargo',
            'telefone': 'Telefone',
            'salario': 'Salário',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Funcionario.objects.filter(username=username).exists():
            raise forms.ValidationError('Já existe um usuário com esse nome. Escolha outro.')
        return username

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        funcionario.set_password(self.cleaned_data['password'])
        if commit:
            funcionario.save()
        return funcionario