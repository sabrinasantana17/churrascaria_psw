from django import forms
from .models import ItemPedido


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['pedido', 'item', 'quantidade', 'preco_conjunto', 'observacao']
        labels = {
            'pedido': 'Pedido',
            'item': 'Item',
            'quantidade': 'Quantidade',
            'preco_conjunto': 'Preço (conjunto)',
            'observacao': 'Observação',
        }