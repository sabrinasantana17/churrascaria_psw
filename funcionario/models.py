from django.db import models
from django.contrib.auth.models import User


class Funcionario(User):
    class Cargo(models.TextChoices):
        GARCOM = 'GARCOM', 'Garçom'
        COZINHEIRO = 'COZINHEIRO', 'Cozinheiro'
        CHURRASQUEIRO = 'CHURRASQUEIRO', 'Churrasqueiro'
        GERENTE = 'GERENTE', 'Gerente'
        CAIXA = 'CAIXA', 'Caixa'

    cargo = models.CharField(max_length=20, choices=Cargo.choices)
    telefone = models.CharField(max_length=20, blank=True)

    def cadastrar(self):
        self.save()
        return self

    def atualizar_perfil(self, **kwargs):
        for campo, valor in kwargs.items():
            setattr(self, campo, valor)
        self.save()
        return self

    @classmethod
    def consultar(cls, pk):
        return cls.objects.filter(pk=pk).first()

    def excluir(self):
        self.delete()
        return True

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_cargo_display()})"
