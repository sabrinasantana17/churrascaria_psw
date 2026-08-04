# Register your models here.
from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'cargo', 'telefone', 'is_active')
    list_filter = ('cargo',)
    search_fields = ('username', 'telefone')