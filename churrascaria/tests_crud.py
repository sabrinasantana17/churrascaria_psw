"""Testes do CRUD completo (editar e excluir) de todos os apps.

Rodar:  python manage.py test churrascaria.tests_crud
"""
from decimal import Decimal

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from cliente.grupo import garantir_grupo_cliente
from cliente.models import Cliente
from feedback.models import Feedback
from funcionario.grupo import garantir_grupo_funcionario
from funcionario.models import Funcionario
from item.models import Item
from itempedido.models import ItemPedido
from pedido.models import Pedido

SENHA = 'senha12345'


def criar_cliente(username):
    cliente = Cliente(username=username)
    cliente.set_password(SENHA)
    cliente.save()
    garantir_grupo_cliente(cliente)
    return cliente


def criar_funcionario(username, cargo):
    funcionario = Funcionario(username=username, cargo=cargo)
    funcionario.set_password(SENHA)
    funcionario.save()
    garantir_grupo_funcionario(funcionario)
    return funcionario


class Base(TestCase):
    def setUp(self):
        self.gerente = criar_funcionario('gerente', 'GERENTE')
        self.garcom = criar_funcionario('garcom', 'GARÇOM')
        self.cozinheiro = criar_funcionario('cozinheiro', 'COZINHEIRO')
        self.ana = criar_cliente('ana')
        self.bia = criar_cliente('bia')
        self.picanha = Item.objects.create(nome='Picanha', preco=Decimal('50.00'), categoria='CARNE')
        self.suco = Item.objects.create(nome='Suco', preco=Decimal('8.00'), categoria='BEBIDA')

    def entrar(self, usuario):
        self.client.force_login(usuario)

    def pedido_com_item(self, cliente, item=None, quantidade=1, **extra):
        item = item or self.picanha
        pedido = Pedido.objects.create(cliente=cliente, **extra)
        ip = ItemPedido.objects.create(
            pedido=pedido, item=item, quantidade=quantidade,
            preco_conjunto=item.preco * quantidade,
        )
        pedido.refresh_from_db()
        return pedido, ip


class PaginasTest(Base):
    """Toda tela nova precisa abrir (pega erro de template/URL)."""

    def test_gerente_abre_todas_as_telas_de_edicao_e_exclusao(self):
        pedido, ip = self.pedido_com_item(self.ana)
        feedback = Feedback.objects.create(usuario=self.ana, mensagem='Muito bom o atendimento!')
        self.entrar(self.gerente)
        urls = [
            reverse('cliente_update', args=[self.bia.pk]),
            reverse('cliente_delete', args=[self.bia.pk]),
            reverse('funcionario_update', args=[self.garcom.pk]),
            reverse('funcionario_delete', args=[self.garcom.pk]),
            reverse('item_update', args=[self.suco.pk]),
            reverse('item_delete', args=[self.suco.pk]),
            reverse('pedido_update', args=[pedido.pk]),
            reverse('pedido_delete', args=[pedido.pk]),
            reverse('itempedido_update', args=[ip.pk]),
            reverse('itempedido_delete', args=[ip.pk]),
            reverse('feedback_update', args=[feedback.pk]),
            reverse('feedback_delete', args=[feedback.pk]),
            # listagens e detalhes (agora com botões)
            reverse('cliente_list'), reverse('cliente_detail', args=[self.ana.pk]),
            reverse('funcionario_list'), reverse('funcionario_detail', args=[self.garcom.pk]),
            reverse('item_list'), reverse('item_detail', args=[self.picanha.pk]),
            reverse('pedido_list'), reverse('pedido_detail', args=[pedido.pk]),
            reverse('itempedido_list'), reverse('itempedido_detail', args=[ip.pk]),
            reverse('feedback_list'), reverse('feedback_detail', args=[feedback.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_cliente_abre_perfil_e_telas_do_proprio_pedido(self):
        pedido, ip = self.pedido_com_item(self.ana)
        self.entrar(self.ana)
        for url in [
            reverse('cliente_detail', args=[self.ana.pk]),
            reverse('cliente_update', args=[self.ana.pk]),
            reverse('cliente_delete', args=[self.ana.pk]),
            reverse('pedido_list'), reverse('pedido_detail', args=[pedido.pk]),
            reverse('pedido_delete', args=[pedido.pk]),
            reverse('itempedido_update', args=[ip.pk]),
            reverse('itempedido_delete', args=[ip.pk]),
        ]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_menu_do_cliente_tem_meu_perfil(self):
        self.entrar(self.ana)
        resposta = self.client.get(reverse('item_list'))
        self.assertContains(resposta, reverse('cliente_detail', args=[self.ana.pk]))


class GruposTest(Base):
    def test_gerente_tem_crud_completo(self):
        gerente = User.objects.get(pk=self.gerente.pk)
        for perm in ['item.change_item', 'item.delete_item', 'cliente.change_cliente',
                     'cliente.delete_cliente', 'funcionario.change_funcionario',
                     'funcionario.delete_funcionario', 'pedido.change_pedido',
                     'pedido.delete_pedido', 'itempedido.change_itempedido',
                     'itempedido.delete_itempedido', 'feedback.change_feedback',
                     'feedback.delete_feedback']:
            with self.subTest(perm=perm):
                self.assertTrue(gerente.has_perm(perm))

    def test_grupo_antigo_sem_permissoes_novas_e_atualizado_no_login(self):
        # Simula um banco antigo: grupo Gerente só com permissões de "ver".
        Group.objects.get(name='Gerente').permissions.set(
            Permission.objects.filter(codename__in=['view_item', 'view_pedido']))
        self.client.post(reverse('login'), {'username': 'gerente', 'password': SENHA})
        gerente = User.objects.get(pk=self.gerente.pk)
        self.assertTrue(gerente.has_perm('item.delete_item'))


class ClienteCrudTest(Base):
    def dados(self, **extra):
        dados = {'username': 'ana', 'first_name': 'Ana', 'last_name': 'Souza',
                 'email': 'ana@x.com', 'telefone': '77999999999', 'password': ''}
        dados.update(extra)
        return dados

    def test_cliente_edita_o_proprio_perfil_sem_trocar_a_senha(self):
        self.entrar(self.ana)
        resposta = self.client.post(reverse('cliente_update', args=[self.ana.pk]), self.dados())
        self.assertRedirects(resposta, reverse('cliente_detail', args=[self.ana.pk]))
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.last_name, 'Souza')
        self.assertTrue(self.ana.check_password(SENHA))  # senha em branco = mantém

    def test_cliente_troca_a_propria_senha_e_continua_logado(self):
        self.entrar(self.ana)
        self.client.post(reverse('cliente_update', args=[self.ana.pk]),
                         self.dados(password='nova-senha-987'))
        self.ana.refresh_from_db()
        self.assertTrue(self.ana.check_password('nova-senha-987'))
        self.assertEqual(self.client.get(reverse('item_list')).status_code, 200)

    def test_cliente_nao_edita_nem_ve_outro_cliente(self):
        self.entrar(self.ana)
        self.assertEqual(self.client.get(reverse('cliente_update', args=[self.bia.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('cliente_delete', args=[self.bia.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('cliente_detail', args=[self.bia.pk])).status_code, 403)

    def test_usuario_repetido_e_recusado_na_edicao(self):
        self.entrar(self.ana)
        resposta = self.client.post(reverse('cliente_update', args=[self.ana.pk]),
                                    self.dados(username='bia'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Já existe um usuário')
        self.ana.refresh_from_db()
        self.assertEqual(self.ana.username, 'ana')

    def test_gerente_exclui_cliente_sem_pedidos(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('cliente_delete', args=[self.bia.pk]))
        self.assertRedirects(resposta, reverse('cliente_list'))
        self.assertFalse(User.objects.filter(username='bia').exists())

    def test_cliente_com_pedidos_nao_e_excluido(self):
        Pedido.objects.create(cliente=self.ana)
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('cliente_delete', args=[self.ana.pk]))
        self.assertRedirects(resposta, reverse('cliente_detail', args=[self.ana.pk]))
        self.assertTrue(Cliente.objects.filter(pk=self.ana.pk).exists())

    def test_cliente_exclui_a_propria_conta(self):
        self.entrar(self.bia)
        resposta = self.client.post(reverse('cliente_delete', args=[self.bia.pk]))
        self.assertRedirects(resposta, reverse('login'))
        self.assertFalse(User.objects.filter(username='bia').exists())

    def test_garcom_edita_cliente_mas_nao_exclui(self):
        self.entrar(self.garcom)
        resposta = self.client.post(reverse('cliente_update', args=[self.bia.pk]),
                                    self.dados(username='bia', first_name='Beatriz'))
        self.assertEqual(resposta.status_code, 302)
        self.bia.refresh_from_db()
        self.assertEqual(self.bia.first_name, 'Beatriz')
        self.assertEqual(self.client.get(reverse('cliente_delete', args=[self.bia.pk])).status_code, 403)


class FuncionarioCrudTest(Base):
    def dados(self, username, cargo, **extra):
        dados = {'username': username, 'first_name': '', 'last_name': '', 'email': '',
                 'cargo': cargo, 'telefone': '', 'salario': '1500.00', 'password': ''}
        dados.update(extra)
        return dados

    def test_gerente_edita_funcionario_e_troca_de_grupo(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('funcionario_update', args=[self.cozinheiro.pk]),
                                    self.dados('cozinheiro', 'GARÇOM'))
        self.assertRedirects(resposta, reverse('funcionario_detail', args=[self.cozinheiro.pk]))
        self.cozinheiro.refresh_from_db()
        self.assertEqual(self.cozinheiro.cargo, 'GARÇOM')
        self.assertEqual(self.cozinheiro.salario, Decimal('1500.00'))
        self.assertEqual(set(self.cozinheiro.groups.values_list('name', flat=True)), {'Garçom'})
        self.assertTrue(self.cozinheiro.check_password(SENHA))

    def test_garcom_nao_mexe_em_funcionarios(self):
        self.entrar(self.garcom)
        self.assertEqual(self.client.get(reverse('funcionario_update', args=[self.cozinheiro.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('funcionario_delete', args=[self.cozinheiro.pk])).status_code, 403)

    def test_gerente_nao_exclui_a_si_mesmo(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('funcionario_delete', args=[self.gerente.pk]))
        self.assertRedirects(resposta, reverse('funcionario_detail', args=[self.gerente.pk]))
        self.assertTrue(Funcionario.objects.filter(pk=self.gerente.pk).exists())

    def test_excluir_funcionario_mantem_o_pedido_sem_atendente(self):
        pedido = Pedido.objects.create(cliente=self.ana, funcionario=self.cozinheiro)
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('funcionario_delete', args=[self.cozinheiro.pk]))
        self.assertRedirects(resposta, reverse('funcionario_list'))
        pedido.refresh_from_db()
        self.assertIsNone(pedido.funcionario)


class ItemCrudTest(Base):
    def test_gerente_edita_item(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('item_update', args=[self.picanha.pk]), {
            'nome': 'Picanha Premium', 'descricao': '', 'preco': '60.00',
            'categoria': 'CARNE', 'disponivel': 'on',
        })
        self.assertRedirects(resposta, reverse('item_detail', args=[self.picanha.pk]))
        self.picanha.refresh_from_db()
        self.assertEqual(self.picanha.nome, 'Picanha Premium')
        self.assertEqual(self.picanha.preco, Decimal('60.00'))

    def test_garcom_nao_edita_nem_exclui_item(self):
        self.entrar(self.garcom)
        self.assertEqual(self.client.get(reverse('item_update', args=[self.picanha.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('item_delete', args=[self.picanha.pk])).status_code, 403)

    def test_gerente_exclui_item_sem_uso(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('item_delete', args=[self.suco.pk]))
        self.assertRedirects(resposta, reverse('item_list'))
        self.assertFalse(Item.objects.filter(pk=self.suco.pk).exists())

    def test_item_que_ja_esta_em_pedido_nao_e_excluido(self):
        self.pedido_com_item(self.ana, self.picanha)
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('item_delete', args=[self.picanha.pk]))
        self.assertRedirects(resposta, reverse('item_detail', args=[self.picanha.pk]))
        self.assertTrue(Item.objects.filter(pk=self.picanha.pk).exists())


class PedidoCrudTest(Base):
    def test_cliente_cancela_o_proprio_pedido_em_andamento(self):
        pedido, _ = self.pedido_com_item(self.ana)
        self.entrar(self.ana)
        resposta = self.client.post(reverse('pedido_delete', args=[pedido.pk]))
        self.assertRedirects(resposta, reverse('pedido_list'))
        self.assertFalse(Pedido.objects.filter(pk=pedido.pk).exists())
        self.assertFalse(ItemPedido.objects.exists())  # itens vão junto

    def test_cliente_nao_cancela_pedido_ja_enviado(self):
        pedido, _ = self.pedido_com_item(self.ana, concluido=True)
        self.entrar(self.ana)
        resposta = self.client.post(reverse('pedido_delete', args=[pedido.pk]))
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        self.assertTrue(Pedido.objects.filter(pk=pedido.pk).exists())

    def test_cliente_nao_mexe_no_pedido_de_outro(self):
        pedido, _ = self.pedido_com_item(self.bia)
        self.entrar(self.ana)
        self.assertEqual(self.client.get(reverse('pedido_delete', args=[pedido.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('pedido_update', args=[pedido.pk])).status_code, 403)

    def test_cliente_nao_edita_os_dados_do_pedido(self):
        pedido, _ = self.pedido_com_item(self.ana)
        self.entrar(self.ana)
        self.assertEqual(self.client.get(reverse('pedido_update', args=[pedido.pk])).status_code, 403)

    def test_equipe_marca_pagamento_e_reabre_pedido(self):
        pedido, _ = self.pedido_com_item(self.ana, concluido=True)
        self.entrar(self.cozinheiro)
        resposta = self.client.post(reverse('pedido_update', args=[pedido.pk]), {
            'funcionario': self.cozinheiro.pk, 'pagamento_efetuado': 'on',  # 'concluido' fora = reabrir
        })
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        pedido.refresh_from_db()
        self.assertTrue(pedido.pagamento_efetuado)
        self.assertFalse(pedido.concluido)
        self.assertEqual(pedido.funcionario_id, self.cozinheiro.pk)

    def test_cozinheiro_nao_exclui_pedido_mas_garcom_sim(self):
        pedido, _ = self.pedido_com_item(self.ana, concluido=True)
        self.entrar(self.cozinheiro)
        self.assertEqual(self.client.get(reverse('pedido_delete', args=[pedido.pk])).status_code, 403)
        self.entrar(self.garcom)
        resposta = self.client.post(reverse('pedido_delete', args=[pedido.pk]))
        self.assertRedirects(resposta, reverse('pedido_list'))
        self.assertFalse(Pedido.objects.filter(pk=pedido.pk).exists())


class ItemPedidoCrudTest(Base):
    def test_cliente_edita_quantidade_e_o_total_e_recalculado(self):
        pedido, ip = self.pedido_com_item(self.ana, self.picanha, 1)
        self.entrar(self.ana)
        resposta = self.client.post(reverse('itempedido_update', args=[ip.pk]),
                                    {'quantidade': 3, 'observacao': 'bem passada'})
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        ip.refresh_from_db()
        pedido.refresh_from_db()
        self.assertEqual(ip.quantidade, 3)
        self.assertEqual(ip.observacao, 'bem passada')
        self.assertEqual(ip.preco_conjunto, Decimal('150.00'))
        self.assertEqual(pedido.valor_total, Decimal('150.00'))

    def test_quantidade_zero_e_recusada(self):
        _, ip = self.pedido_com_item(self.ana)
        self.entrar(self.ana)
        resposta = self.client.post(reverse('itempedido_update', args=[ip.pk]),
                                    {'quantidade': 0, 'observacao': ''})
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'pelo menos 1')
        ip.refresh_from_db()
        self.assertEqual(ip.quantidade, 1)

    def test_cliente_remove_item_e_o_total_e_recalculado(self):
        pedido, ip = self.pedido_com_item(self.ana, self.picanha, 1)
        ItemPedido.objects.create(pedido=pedido, item=self.suco, quantidade=2,
                                  preco_conjunto=Decimal('16.00'))
        pedido.refresh_from_db()
        self.assertEqual(pedido.valor_total, Decimal('66.00'))
        self.entrar(self.ana)
        resposta = self.client.post(reverse('itempedido_delete', args=[ip.pk]))
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        pedido.refresh_from_db()
        self.assertEqual(pedido.valor_total, Decimal('16.00'))

    def test_cliente_nao_altera_item_de_pedido_ja_enviado(self):
        pedido, ip = self.pedido_com_item(self.ana, concluido=True)
        self.entrar(self.ana)
        resposta = self.client.post(reverse('itempedido_update', args=[ip.pk]),
                                    {'quantidade': 9, 'observacao': ''})
        self.assertRedirects(resposta, reverse('pedido_detail', args=[pedido.pk]))
        ip.refresh_from_db()
        self.assertEqual(ip.quantidade, 1)
        self.client.post(reverse('itempedido_delete', args=[ip.pk]))
        self.assertTrue(ItemPedido.objects.filter(pk=ip.pk).exists())

    def test_cliente_nao_altera_item_de_outro_cliente(self):
        _, ip = self.pedido_com_item(self.bia)
        self.entrar(self.ana)
        self.assertEqual(self.client.get(reverse('itempedido_update', args=[ip.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('itempedido_delete', args=[ip.pk])).status_code, 403)

    def test_equipe_altera_item_mesmo_com_pedido_enviado(self):
        _, ip = self.pedido_com_item(self.ana, concluido=True)
        self.entrar(self.garcom)
        resposta = self.client.post(reverse('itempedido_update', args=[ip.pk]),
                                    {'quantidade': 2, 'observacao': ''})
        self.assertEqual(resposta.status_code, 302)
        ip.refresh_from_db()
        self.assertEqual(ip.quantidade, 2)

    def test_detalhe_do_pedido_mostra_botoes_dos_itens_ao_dono(self):
        pedido, ip = self.pedido_com_item(self.ana)
        self.entrar(self.ana)
        resposta = self.client.get(reverse('pedido_detail', args=[pedido.pk]))
        self.assertContains(resposta, reverse('itempedido_update', args=[ip.pk]))
        self.assertContains(resposta, reverse('itempedido_delete', args=[ip.pk]))


class FeedbackCrudTest(Base):
    def setUp(self):
        super().setUp()
        self.feedback = Feedback.objects.create(usuario=self.ana, tipo='ELOGIO',
                                                mensagem='Atendimento excelente!')

    def test_autor_edita_o_feedback_enquanto_nao_respondido(self):
        self.entrar(self.ana)
        resposta = self.client.post(reverse('feedback_update', args=[self.feedback.pk]),
                                    {'tipo': 'SUGESTAO', 'mensagem': 'Poderia ter mais sobremesas.'})
        self.assertRedirects(resposta, reverse('feedback_detail', args=[self.feedback.pk]))
        self.feedback.refresh_from_db()
        self.assertEqual(self.feedback.tipo, 'SUGESTAO')
        self.assertEqual(self.feedback.mensagem, 'Poderia ter mais sobremesas.')

    def test_autor_nao_edita_feedback_ja_respondido(self):
        self.feedback.respondido = True
        self.feedback.save()
        self.entrar(self.ana)
        resposta = self.client.post(reverse('feedback_update', args=[self.feedback.pk]),
                                    {'tipo': 'OUTRO', 'mensagem': 'Mudando o texto depois de respondido'})
        self.assertRedirects(resposta, reverse('feedback_detail', args=[self.feedback.pk]))
        self.feedback.refresh_from_db()
        self.assertEqual(self.feedback.mensagem, 'Atendimento excelente!')

    def test_gerente_marca_como_respondido_sem_mexer_no_texto(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('feedback_update', args=[self.feedback.pk]),
                                    {'respondido': 'on', 'mensagem': 'texto alterado pelo gerente'})
        self.assertRedirects(resposta, reverse('feedback_detail', args=[self.feedback.pk]))
        self.feedback.refresh_from_db()
        self.assertTrue(self.feedback.respondido)
        self.assertEqual(self.feedback.mensagem, 'Atendimento excelente!')

    def test_outro_usuario_nao_ve_edita_nem_exclui(self):
        self.entrar(self.bia)
        for nome in ['feedback_detail', 'feedback_update', 'feedback_delete']:
            with self.subTest(view=nome):
                self.assertEqual(self.client.get(reverse(nome, args=[self.feedback.pk])).status_code, 403)

    def test_autor_exclui_o_proprio_feedback(self):
        self.entrar(self.ana)
        resposta = self.client.post(reverse('feedback_delete', args=[self.feedback.pk]))
        self.assertRedirects(resposta, reverse('feedback_list'))
        self.assertFalse(Feedback.objects.filter(pk=self.feedback.pk).exists())

    def test_gerente_exclui_qualquer_feedback(self):
        self.entrar(self.gerente)
        resposta = self.client.post(reverse('feedback_delete', args=[self.feedback.pk]))
        self.assertRedirects(resposta, reverse('feedback_list'))
        self.assertFalse(Feedback.objects.filter(pk=self.feedback.pk).exists())

    def test_get_nunca_exclui(self):
        self.entrar(self.ana)
        self.client.get(reverse('feedback_delete', args=[self.feedback.pk]))
        self.assertTrue(Feedback.objects.filter(pk=self.feedback.pk).exists())
