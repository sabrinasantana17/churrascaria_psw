from django.db import models
from django.db.models import Sum
from cliente.models import Cliente
from funcionario.models import Funcionario
from item.models import Item


class Pedido(models.Model):

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='pedidos_atendidos')
    pagamento_efetuado = models.BooleanField(default=False)
    concluido = models.BooleanField(default=False)  # False = cliente ainda montando; True = pedido enviado
    criado_em = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    itens = models.ManyToManyField(Item, through='itempedido.ItemPedido', related_name='pedidos')

    def recalcular_total(self):
        """Soma o valor de todos os itens do pedido e guarda em valor_total."""
        total = self.itempedido_set.aggregate(total=Sum('preco_conjunto'))['total'] or 0
        self.valor_total = total
        self.save(update_fields=['valor_total'])

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"
