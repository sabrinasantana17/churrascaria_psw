# Register your models here.
from django.contrib import admin
from .models import ItemPedido


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('id','pedido', 'item', 'quantidade', 'preco_conjunto', 'observacao')