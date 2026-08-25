from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):

    CATEGORIA_CHOICES = [
        ('CARNE', 'Carne'),
        ('ACOMPANHAMENTO', 'Acompanhamento'),
        ('BEBIDA', 'Bebida'),
        ('SOBREMESA', 'Sobremesa'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    disponivel = models.BooleanField(default=True)
   
    def __str__(self):
        return self.nome
