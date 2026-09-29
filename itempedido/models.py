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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Sempre que um item entra/muda, o total do pedido é recalculado.
        self.pedido.recalcular_total()

    def delete(self, *args, **kwargs):
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido.recalcular_total()

    def __str__(self):
        return f"{self.quantidade}x {self.item.nome}"