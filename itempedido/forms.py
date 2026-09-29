from django import forms
from cliente.models import Cliente
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


class AdicionarItemForm(forms.ModelForm):
    """Formulário da tela 'Itens do pedido'. Para funcionários/administradores
    (mostrar_cliente=True) aparece também a escolha do cliente do pedido."""

    class Meta:
        model = ItemPedido
        fields = ['quantidade', 'observacao']
        labels = {
            'quantidade': 'Quantidade',
            'observacao': 'Observação (ex.: tirar a cebola)',
        }

    def __init__(self, *args, mostrar_cliente=False, **kwargs):
        super().__init__(*args, **kwargs)
        if mostrar_cliente:
            campo = forms.ModelChoiceField(
                queryset=Cliente.objects.order_by('username'),
                label='Cliente do pedido',
                empty_label='Selecione o cliente',
            )
            campo.label_from_instance = lambda c: c.get_full_name() or c.username
            self.fields['cliente'] = campo
            self.order_fields(['cliente', 'quantidade', 'observacao'])

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']
        if quantidade < 1:
            raise forms.ValidationError('A quantidade deve ser pelo menos 1.')
        return quantidade
