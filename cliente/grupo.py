from django.contrib.auth.models import Group, Permission

# O que um cliente precisa para usar o sistema: ver o cardápio e fazer/ver os
# próprios pedidos (a filtragem "só os meus pedidos" é feita na view).
PERMISSOES_CLIENTE = [
    ('item', 'view_item'),
    ('pedido', 'view_pedido'),
    ('pedido', 'add_pedido'),
]


def garantir_grupo_cliente(usuario):
    """Coloca o usuário no grupo 'Cliente' e garante que o grupo tenha as
    permissões básicas (assim funciona até num banco de dados novo, sem
    precisar configurar o grupo no admin)."""
    grupo, _ = Group.objects.get_or_create(name='Cliente')
    for app_label, codename in PERMISSOES_CLIENTE:
        permissao = Permission.objects.filter(
            content_type__app_label=app_label, codename=codename
        ).first()
        if permissao:
            grupo.permissions.add(permissao)
    usuario.groups.add(grupo)


def garantir_grupo_ao_logar(sender, request, user, **kwargs):
    """Roda em todo login: se a pessoa é Cliente mas ainda não está em nenhum
    grupo (ex.: foi criada pelo admin), ela entra no grupo Cliente."""
    if hasattr(user, 'cliente') and not user.groups.exists():
        garantir_grupo_cliente(user)
