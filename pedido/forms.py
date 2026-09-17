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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        cliente_do_usuario = getattr(user, 'cliente', None)
        if cliente_do_usuario is not None:
            # Quem está fazendo o pedido é o próprio cliente: ele não escolhe
            # pra quem é o pedido (é sempre ele mesmo), nem quem vai atender,
            # nem marca se o pagamento já foi feito — isso é tarefa da equipe.
            del self.fields['cliente']
            del self.fields['funcionario']
            del self.fields['pagamento_efetuado']
        else:
            funcionario_do_usuario = getattr(user, 'funcionario', None)
            if funcionario_do_usuario is not None:
                self.fields['funcionario'].initial = funcionario_do_usuario