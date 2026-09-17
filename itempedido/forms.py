from django import forms
from pedido.models import Pedido
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        cliente_do_usuario = getattr(user, 'cliente', None)
        if cliente_do_usuario is not None:
            # Cliente só pode lançar itens nos próprios pedidos.
            self.fields['pedido'].queryset = Pedido.objects.filter(
                cliente=cliente_do_usuario
            ).order_by('-criado_em')