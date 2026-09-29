from django.contrib.auth.models import Group, Permission

# Permissões básicas para trabalhar com pedidos pelo cardápio.
_PEDIDOS = [
    ('item', 'view_item'),
    ('pedido', 'view_pedido'),
    ('pedido', 'add_pedido'),
    ('pedido', 'change_pedido'),
    ('itempedido', 'view_itempedido'),
    ('itempedido', 'add_itempedido'),
    ('pedido', 'change_pedido'),
    ('itempedido', 'view_itempedido'),
    ('itempedido', 'add_itempedido'),
    ('itempedido', 'change_itempedido'),
]

_EXCLUIR_PEDIDOS = [
    ('pedido', 'delete_pedido'),
    ('itempedido', 'delete_itempedido'),
]

# Permissões padrão de cada cargo (CRUD: view = ver/detalhar, add = criar,
# change = editar, delete = excluir). Elas são GARANTIDAS a cada login: se
# faltar alguma, ela é adicionada ao grupo. Para dar mais poder a um cargo,
# acrescente a permissão aqui.
PERMISSOES_PADRAO = {
    'Gerente': _PEDIDOS + _EXCLUIR_PEDIDOS + [
        ('item', 'add_item'),
        ('item', 'change_item'),
        ('item', 'delete_item'),
        ('cliente', 'view_cliente'),
        ('cliente', 'add_cliente'),
        ('cliente', 'change_cliente'),
        ('cliente', 'delete_cliente'),
        ('funcionario', 'view_funcionario'),
        ('funcionario', 'add_funcionario'),
        ('funcionario', 'change_funcionario'),
        ('funcionario', 'delete_funcionario'),
        ('feedback', 'view_feedback'),
        ('feedback', 'change_feedback'),
        ('feedback', 'delete_feedback'),
    ],
    'Garçom': _PEDIDOS + _EXCLUIR_PEDIDOS + [
        ('cliente', 'view_cliente'),
        ('cliente', 'add_cliente'),
        ('cliente', 'change_cliente'),
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
>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37
    ],
    'Cozinheiro': _PEDIDOS,
}


def garantir_grupo_funcionario(funcionario):
    """Coloca o funcionário no grupo do seu cargo (Gerente, Garçom ou
    Cozinheiro) e garante que o grupo tenha as permissões padrão do cargo."""
    nome_grupo = funcionario.get_cargo_display()
    grupo, _ = Group.objects.get_or_create(name=nome_grupo)
    Cozinheiro) e garante que o grupo tenha as permissões padrão do cargo."""
    nome_grupo = funcionario.get_cargo_display()
    grupo, _ = Group.objects.get_or_create(name=nome_grupo)
    for app_label, codename in PERMISSOES_PADRAO.get(nome_grupo, []):
        permissao = Permission.objects.filter(
            content_type__app_label=app_label, codename=codename
        ).first()
        if permissao:
            grupo.permissions.add(permissao)
    funcionario.groups.add(grupo)


def atualizar_grupo_funcionario(funcionario):
    """Usado ao EDITAR: se o cargo mudou, tira dos grupos de cargo antigos e
    coloca no do cargo novo (outros grupos que a pessoa tenha ficam intactos)."""
    from .models import Funcionario
    nomes_de_cargo = [nome for _, nome in Funcionario.CARGO_CHOICES]
    funcionario.groups.remove(*Group.objects.filter(name__in=nomes_de_cargo))
    garantir_grupo_funcionario(funcionario)


def garantir_grupo_ao_logar(sender, request, user, **kwargs):
    """Roda em todo login: garante que o funcionário está no grupo do cargo
    e que esse grupo tem as permissões padrão."""
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
>>>>>>> df0c0425aa9c69d3c1990050c85afe59644dca37
    funcionario = getattr(user, 'funcionario', None)
    if funcionario is not None:
        garantir_grupo_funcionario(funcionario)
