from django.db import models
from cliente.models import Cliente
from funcionario.models import Funcionario
from item.models import Item


class Pedido(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='pedidos_atendidos')
    pagamento_efetuado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    itens = models.ManyToManyField(Item, through='itempedido.ItemPedido', related_name='pedidos')

   

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"