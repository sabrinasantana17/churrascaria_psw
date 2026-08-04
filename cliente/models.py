from django.db import models
from django.contrib.auth.models import User


class Cliente(User):
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
        return self.get_full_name() or self.username
