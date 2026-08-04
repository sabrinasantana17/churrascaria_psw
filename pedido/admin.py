# Register your models here.
from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'funcionario', 'status', 'criado_em', 'valor_total')
    list_filter = ('status', 'criado_em')
    search_fields = ('cliente__username',)