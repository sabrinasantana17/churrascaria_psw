# Register your models here.
from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefone', 'is_active')
    search_fields = ('username', 'email', 'telefone')