def pode_montar_pedido(usuario):
    """Quem pode montar pedidos pelo cardápio: o próprio cliente ou qualquer
    funcionário/administrador com a permissão de criar pedidos."""
    return hasattr(usuario, 'cliente') or usuario.has_perm('pedido.add_pedido')
<<<<<<< HEAD


def e_dono_do_pedido(usuario, pedido):
    cliente = getattr(usuario, 'cliente', None)
    return cliente is not None and pedido.cliente_id == cliente.pk


def pode_alterar_pedido(usuario, pedido):
    """Editar os dados do pedido (atendente, pagamento, reabrir) é da equipe.
    O cliente altera o pedido mexendo nos itens (ver pode_alterar_item_pedido)."""
    return usuario.has_perm('pedido.change_pedido')


def pode_excluir_pedido(usuario, pedido):
    """Equipe com permissão exclui qualquer pedido; o cliente só cancela o
    próprio pedido enquanto ele ainda está em andamento."""
    if usuario.has_perm('pedido.delete_pedido'):
        return True
    return e_dono_do_pedido(usuario, pedido) and not pedido.concluido


def pode_alterar_item_pedido(usuario, item_pedido):
    if usuario.has_perm('itempedido.change_itempedido'):
        return True
    pedido = item_pedido.pedido
    return e_dono_do_pedido(usuario, pedido) and not pedido.concluido


def pode_excluir_item_pedido(usuario, item_pedido):
    if usuario.has_perm('itempedido.delete_itempedido'):
        return True
    pedido = item_pedido.pedido
    return e_dono_do_pedido(usuario, pedido) and not pedido.concluido
=======
>>>>>>> f2b373a033f1ba172e6d374f236fdae65653d641
