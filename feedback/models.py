from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):

    TIPO_CHOICES = [
        ('SUGESTAO', 'Sugestão de melhoria'),
        ('PROBLEMA', 'Problema / erro no sistema'),
        ('ELOGIO', 'Elogio'),
        ('OUTRO', 'Outro'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='SUGESTAO')
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f"Feedback #{self.id} - {self.usuario.get_full_name() or self.usuario.username}"