from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'tipo', 'criado_em', 'respondido')
    list_filter = ('tipo', 'respondido')
    search_fields = ('mensagem', 'usuario__username')