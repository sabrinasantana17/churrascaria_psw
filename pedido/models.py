from django.db import models
from cliente.models import Cliente
from funcionario.models import Funcionario
from item.models import Item


class Pedido(models.Model):
    class Status(models.TextChoices):
        ABERTO = 'ABERTO', 'Aberto'
        EM_PREPARO = 'EM_PREPARO', 'Em preparo'
        FINALIZADO = 'FINALIZADO', 'Finalizado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='pedidos_atendidos')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO)
    criado_em = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    itens = models.ManyToManyField(Item, through='itempedido.ItemPedido', related_name='pedidos')

    def criar_pedido(self):
        self.save()
        return self

    def atualizar_status(self, status: str):
        self.status = status
        self.save()

    def calcular_total(self):
        total = sum(item.calcular_subtotal() for item in self.itempedido_set.all())
        self.valor_total = total
        self.save()
        return total

    def cancelar(self):
        self.status = self.Status.CANCELADO
        self.save()
        return True

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"