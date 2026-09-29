def pode_montar_pedido(usuario):
    """Quem pode montar pedidos pelo cardápio: o próprio cliente ou qualquer
    funcionário/administrador com a permissão de criar pedidos."""
    return hasattr(usuario, 'cliente') or usuario.has_perm('pedido.add_pedido')
