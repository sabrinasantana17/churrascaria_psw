from django.db import models
from django.contrib.auth.models import User


class Funcionario(User):

    CARGO_CHOICES = [
        ('GERENTE', 'Gerente'),
        ('VENDEDOR', 'Vendedor'),
        ('CAIXA', 'Caixa'),
    ]

    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    telefone = models.CharField(max_length=20, blank=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_cargo_display()})"
