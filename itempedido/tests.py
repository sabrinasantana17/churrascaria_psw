from decimal import Decimal

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from cliente.models import Cliente
from funcionario.grupo import garantir_grupo_funcionario
from funcionario.models import Funcionario
from item.models import Item
from pedido.models import Pedido


def _criar_cliente(username):
    grupo, _ = Group.objects.get_or_create(name='Cliente')
    grupo.permissions.set(Permission.objects.filter(codename__in=[
        'view_item', 'view_pedido', 'add_pedido', 'view_itempedido', 'add_itempedido',
    ]))
    cliente = Cliente(username=username)
    cliente.set_password('senha12345')
    cliente.save()
    cliente.groups.add(grupo)
    return cliente


def _criar_funcionario(username, cargo):
    funcionario = Funcionario(username=username, cargo=cargo)
    funcionario.set_password('senha12345')
    funcionario.save()
    garantir_grupo_funcionario(funcionario)
    return funcionario


class FluxoDoPedidoTest(TestCase):
    def setUp(self):
        self.cliente = _criar_cliente('ana')
        self.picanha = Item.objects.create(nome='Picanha', preco=Decimal('50.00'), categoria='CARNE')
        self.suco = Item.objects.create(nome='Suco', preco=Decimal('8.00'), categoria='BEBIDA')
        self.client.force_login(self.cliente)

    def test_cardapio_mostra_botao_itens_do_pedido(self):
        resposta = self.client.get(reverse('item_list'))
        self.assertContains(resposta, 'Itens do pedido')

    def test_salvar_cria_pedido_em_andamento_com_item_e_total(self):
        resposta = self.client.post(
            reverse('adicionar_item', args=[self.picanha.pk]),
            {'quantidade': 4, 'observacao': 'tirar a cebola'},
        )
        pedido = Pedido.objects.get()
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertFalse(pedido.concluido)
        ip = pedido.itempedido_set.get()
        self.assertEqual(ip.quantidade, 4)
        self.assertEqual(ip.observacao, 'tirar a cebola')
        self.assertEqual(pedido.valor_total, Decimal('200.00'))

    def test_novos_itens_entram_no_mesmo_pedido_e_total_e_a_soma(self):
        self.client.post(reverse('adicionar_item', args=[self.picanha.pk]), {'quantidade': 2})
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'quantidade': 3})
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'quantidade': 1})
        self.assertEqual(Pedido.objects.count(), 1)
        pedido = Pedido.objects.get()
        self.assertEqual(pedido.itempedido_set.count(), 2)
        self.assertEqual(pedido.valor_total, Decimal('132.00'))  # 2x50 + 4x8

    def test_concluir_pedido_envia_e_proximo_item_abre_pedido_novo(self):
        self.client.post(reverse('adicionar_item', args=[self.picanha.pk]), {'quantidade': 1})
        pedido = Pedido.objects.get()
        self.client.post(reverse('concluir_pedido', args=[pedido.pk]))
        pedido.refresh_from_db()
        self.assertTrue(pedido.concluido)
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'quantidade': 1})
        self.assertEqual(Pedido.objects.count(), 2)
        self.assertEqual(pedido.itempedido_set.count(), 1)  # o enviado não recebeu o suco

    def test_nao_conclui_pedido_vazio(self):
        pedido = Pedido.objects.create(cliente=self.cliente)
        self.client.post(reverse('concluir_pedido', args=[pedido.pk]))
        pedido.refresh_from_db()
        self.assertFalse(pedido.concluido)

    def test_cliente_nao_conclui_pedido_de_outro(self):
        outro = _criar_cliente('bia')
        pedido = Pedido.objects.create(cliente=outro)
        resposta = self.client.post(reverse('concluir_pedido', args=[pedido.pk]))
        self.assertEqual(resposta.status_code, 404)

    def test_cliente_so_ve_os_proprios_pedidos(self):
        outro = _criar_cliente('bia')
        Pedido.objects.create(cliente=outro)
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'quantidade': 1})
        resposta = self.client.get(reverse('pedido_list'))
        self.assertEqual(list(resposta.context['pedidos']), list(Pedido.objects.filter(cliente=self.cliente)))

    def test_equipe_ve_todos_os_pedidos_do_mais_recente_ao_mais_antigo(self):
        gerente = _criar_funcionario('chefe', 'GERENTE')
        p1 = Pedido.objects.create(cliente=self.cliente, concluido=True)
        p2 = Pedido.objects.create(cliente=self.cliente, concluido=False)  # ainda montando
        p3 = Pedido.objects.create(cliente=self.cliente, concluido=True)
        self.client.force_login(gerente)
        resposta = self.client.get(reverse('pedido_list'))
        self.assertEqual(list(resposta.context['pedidos']), [p3, p2, p1])


class FluxoDaEquipeTest(TestCase):
    """Gerente, garçom, cozinheiro e administrador também montam pedidos."""

    def setUp(self):
        self.cliente = _criar_cliente('ana')
        self.picanha = Item.objects.create(nome='Picanha', preco=Decimal('50.00'), categoria='CARNE')
        self.suco = Item.objects.create(nome='Suco', preco=Decimal('8.00'), categoria='BEBIDA')

    def _fluxo_completo(self, usuario):
        self.client.force_login(usuario)
        cardapio = self.client.get(reverse('item_list'))
        self.assertContains(cardapio, 'Itens do pedido')

        resposta = self.client.post(
            reverse('adicionar_item', args=[self.picanha.pk]),
            {'cliente': self.cliente.pk, 'quantidade': 2, 'observacao': 'ao ponto'},
        )
        pedido = Pedido.objects.get()
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        self.assertEqual(pedido.cliente, self.cliente)
        self.assertFalse(pedido.concluido)
        self.assertEqual(pedido.valor_total, Decimal('100.00'))

        # segundo item entra no mesmo pedido do mesmo cliente
        self.client.post(
            reverse('adicionar_item', args=[self.suco.pk]),
            {'cliente': self.cliente.pk, 'quantidade': 3},
        )
        pedido.refresh_from_db()
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(pedido.valor_total, Decimal('124.00'))

        detalhe = self.client.get(reverse('pedido_detail', args=[pedido.pk]))
        self.assertContains(detalhe, 'Concluir pedido')

        self.client.post(reverse('concluir_pedido', args=[pedido.pk]))
        pedido.refresh_from_db()
        self.assertTrue(pedido.concluido)
        return pedido

    def test_gerente_monta_e_conclui_pedido(self):
        pedido = self._fluxo_completo(_criar_funcionario('chefe', 'GERENTE'))
        self.assertEqual(pedido.funcionario.username, 'chefe')

    def test_garcom_monta_e_conclui_pedido(self):
        self._fluxo_completo(_criar_funcionario('gar', 'GARÇOM'))

    def test_cozinheiro_monta_e_conclui_pedido(self):
        self._fluxo_completo(_criar_funcionario('coz', 'COZINHEIRO'))

    def test_administrador_monta_e_conclui_pedido(self):
        admin = User.objects.create_superuser('adm', 'a@a.com', 'senha12345')
        pedido = self._fluxo_completo(admin)
        self.assertIsNone(pedido.funcionario)  # superusuário não é funcionário

    def test_funcionario_precisa_escolher_o_cliente(self):
        self.client.force_login(_criar_funcionario('chefe', 'GERENTE'))
        resposta = self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'quantidade': 1})
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Pedido.objects.count(), 0)

    def test_cliente_ja_vem_selecionado_depois_do_primeiro_item(self):
        self.client.force_login(_criar_funcionario('chefe', 'GERENTE'))
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'cliente': self.cliente.pk, 'quantidade': 1})
        resposta = self.client.get(reverse('adicionar_item', args=[self.picanha.pk]))
        self.assertEqual(resposta.context['form'].initial['cliente'], self.cliente.pk)

    def test_usuario_sem_permissao_nao_monta_pedido(self):
        Item.objects.filter(pk=self.suco.pk).update(disponivel=True)
        comum = User.objects.create_user('comum', password='senha12345')
        comum.user_permissions.add(Permission.objects.get(codename='view_item'))
        self.client.force_login(comum)
        self.assertNotContains(self.client.get(reverse('item_list')), 'Itens do pedido')
        self.client.post(reverse('adicionar_item', args=[self.suco.pk]), {'cliente': self.cliente.pk, 'quantidade': 1})
        self.assertEqual(Pedido.objects.count(), 0)

    def test_grupo_do_funcionario_sem_permissoes_e_preenchido_no_login(self):
        garcom = Funcionario(username='sab', cargo='GARÇOM')
        garcom.set_password('senha12345')
        garcom.save()
        grupo = Group.objects.create(name='Garçom')  # grupo criado vazio, como no cadastro antigo
        garcom.groups.add(grupo)
        self.assertFalse(grupo.permissions.exists())
        resposta = self.client.post(reverse('login'), {'username': 'sab', 'password': 'senha12345'}, follow=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Itens do cardápio')
        self.assertTrue(grupo.permissions.filter(codename='add_pedido').exists())
