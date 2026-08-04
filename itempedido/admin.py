# Register your models here.
from django.contrib import admin
from .models import ItemPedido


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'item', 'quantidade', 'preco_unitario', 'observacao')
    search_fields = ('pedido__id', 'item__nome')
    autocomplete_fields = ['item']