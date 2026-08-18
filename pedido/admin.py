# Register your models here.
from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'funcionario', 'pagamento_efetuado', 'criado_em', 'valor_total')