from django.db import models
from django.contrib.auth.models import User


class Cliente(User):
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username
