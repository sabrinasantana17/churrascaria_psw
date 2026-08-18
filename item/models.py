from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    categoria = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)

    
    def __str__(self):
        return self.nome
