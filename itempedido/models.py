from django.db import models
from pedido.models import Pedido
from item.models import Item


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_conjunto  = models.DecimalField(max_digits=8, decimal_places=2)
    observacao = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('pedido', 'item')

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome}"