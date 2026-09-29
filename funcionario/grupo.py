from django.contrib.auth.models import Group, Permission

# Permissões básicas para trabalhar com pedidos pelo cardápio.
_PEDIDOS = [
    ('item', 'view_item'),
    ('pedido', 'view_pedido'),
    ('pedido', 'add_pedido'),
    ('itempedido', 'view_itempedido'),
    ('itempedido', 'add_itempedido'),
]

# Permissões iniciais de cada grupo. Só são aplicadas quando o grupo ainda está
# sem nenhuma permissão; depois disso, o que for ajustado em /admin/ -> Grupos
# é respeitado.
PERMISSOES_PADRAO = {
    'Gerente': _PEDIDOS + [
        ('item', 'add_item'),
        ('cliente', 'view_cliente'),
        ('cliente', 'add_cliente'),
        ('funcionario', 'view_funcionario'),
        ('funcionario', 'add_funcionario'),
        ('feedback', 'view_feedback'),
    ],
    'Garçom': _PEDIDOS + [
        ('cliente', 'view_cliente'),
        ('cliente', 'add_cliente'),
    ],
    'Cozinheiro': _PEDIDOS,
}


def garantir_grupo_funcionario(funcionario):
    """Coloca o funcionário no grupo do seu cargo (Gerente, Garçom ou
    Cozinheiro) e, se o grupo estiver vazio, dá a ele as permissões básicas."""
    nome_grupo = funcionario.get_cargo_display()
    grupo, _ = Group.objects.get_or_create(name=nome_grupo)
    if not grupo.permissions.exists():
        for app_label, codename in PERMISSOES_PADRAO.get(nome_grupo, []):
            permissao = Permission.objects.filter(
                content_type__app_label=app_label, codename=codename
            ).first()
            if permissao:
                grupo.permissions.add(permissao)
    funcionario.groups.add(grupo)


def garantir_grupo_ao_logar(sender, request, user, **kwargs):
    """Roda em todo login: garante que o funcionário está no grupo do cargo
    e que esse grupo tem as permissões básicas."""
    funcionario = getattr(user, 'funcionario', None)
    if funcionario is not None:
        garantir_grupo_funcionario(funcionario)
