from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'funcionario', 'pagamento_efetuado']
        labels = {
            'cliente': 'Cliente',
            'funcionario': 'Funcionário',
            'pagamento_efetuado': 'Pagamento efetuado',
        }