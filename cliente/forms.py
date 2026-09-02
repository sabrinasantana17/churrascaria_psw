from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    class Meta:
        model = Cliente
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone', 'password']
        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Cliente.objects.filter(username=username).exists():
            raise forms.ValidationError('Já existe um usuário com esse nome. Escolha outro.')
        return username

    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.set_password(self.cleaned_data['password'])
        if commit:
            cliente.save()
        return cliente