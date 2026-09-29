from django.test import TestCase
from django.urls import reverse

from cliente.models import Cliente


class LoginDoClienteTest(TestCase):
    def test_cadastro_e_login_levam_ao_cardapio_sem_403(self):
        self.client.post(reverse('cadastro'), {
            'username': 'maria', 'first_name': 'Maria', 'last_name': 'Silva',
            'email': 'm@m.com', 'telefone': '77999999999', 'password': 'senha12345',
        })
        resposta = self.client.post(reverse('login'), {'username': 'maria', 'password': 'senha12345'}, follow=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Itens do cardápio')

    def test_cliente_criado_sem_grupo_entra_no_grupo_ao_logar(self):
        cliente = Cliente(username='joao')  # como se tivesse sido criado pelo admin
        cliente.set_password('senha12345')
        cliente.save()
        self.assertFalse(cliente.groups.exists())
        resposta = self.client.post(reverse('login'), {'username': 'joao', 'password': 'senha12345'}, follow=True)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Itens do cardápio')
        self.assertTrue(cliente.groups.filter(name='Cliente').exists())
