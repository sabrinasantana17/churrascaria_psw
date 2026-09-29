# Churrascaria Fogo e Brasa

Sistema web desenvolvido em Python utilizando o framework Django, destinado ao gerenciamento de pedidos de uma churrascaria, permitindo que o cliente monte o próprio pedido pelo cardápio e que a equipe acompanhe todos os pedidos enviados.

## Sobre o projeto

A Churrascaria Fogo e Brasa é uma plataforma web criada para organizar o atendimento de uma churrascaria de forma simples e prática.

O cliente consulta o cardápio, escolhe os itens, informa a quantidade e observações (por exemplo, "tirar a cebola") e conclui o pedido. O sistema calcula automaticamente o valor de cada item (preço × quantidade) e o total do pedido. A equipe (gerente, garçom e cozinheiro) visualiza os pedidos enviados, do mais recente para o mais antigo.

O acesso às telas é controlado por grupos e permissões do Django, de modo que cada tipo de usuário enxerga apenas o que lhe cabe.

## Objetivos

### Objetivo geral

Desenvolver um sistema web para gerenciar pedidos de uma churrascaria, reduzindo erros de anotação e agilizando o atendimento.

### Objetivos específicos

- Cadastrar clientes, funcionários e itens do cardápio;
- Permitir que o cliente monte o pedido escolhendo itens, quantidade e observações;
- Calcular automaticamente o valor de cada item e o total do pedido;
- Permitir que o cliente conclua (envie) o pedido;
- Permitir que cada cliente consulte apenas os próprios pedidos;
- Permitir que a equipe consulte todos os pedidos enviados, em ordem de horário;
- Controlar o acesso às funcionalidades por grupos e permissões;
- Registrar sugestões, problemas e elogios dos usuários (feedbacks).

## Funcionalidades

- Cadastro e autenticação de usuários (login e logout);
- Cardápio com categorias (Carne, Acompanhamento, Bebida e Sobremesa);
- Tela **Itens do pedido**: quantidade, observação e valor calculado (preço × quantidade);
- Criação automática do pedido ao salvar o primeiro item;
- Total do pedido calculado pela soma dos itens;
- Botão **Concluir pedido** (após concluído, o pedido não recebe mais itens);
- **Meus pedidos** para o cliente;
- Lista de todos os pedidos enviados para a equipe e administradores;
- Cadastro de funcionários por cargo (Gerente, Garçom e Cozinheiro);
- Feedbacks dos usuários;
- Painel administrativo do Django;
- Interface responsiva.

## Tecnologias utilizadas

- Python
- Django
- SQLite
- HTML5
- CSS3
- Bootstrap (tema SB Admin 2)
- JavaScript

## Documentação oficial

Durante o desenvolvimento do projeto foi utilizada como principal referência a documentação oficial do framework Django.

Documentação utilizada:

https://docs.djangoproject.com/en/6.0/

## Arquitetura do projeto

O projeto foi organizado em aplicações Django independentes, favorecendo a modularização e a manutenção do código.

```
churrascaria_psw/
├── churrascaria/      # configurações do projeto
├── cliente/           # clientes e grupo "Cliente"
├── funcionario/       # funcionários (Gerente, Garçom, Cozinheiro)
├── item/              # itens do cardápio
├── pedido/            # pedidos
├── itempedido/        # itens de cada pedido (quantidade, observação, subtotal)
├── feedback/          # feedbacks dos usuários
├── templates/         # páginas HTML
├── static/            # CSS, JavaScript e bibliotecas front-end
├── manage.py
├── requirements.txt
├── diagrama de classe.png
└── README.md
```

## Diagrama de classes

![Diagrama de Classes](diagrama%20de%20classe.png)

Arquivo: [diagrama de classe.png](diagrama%20de%20classe.png)

## Como executar o projeto

### Clonar o repositório

```bash
git clone https://github.com/sabrinasantana17/churrascaria_psw.git
```

### Entrar na pasta

```bash
cd churrascaria_psw
```

### Criar ambiente virtual

**Windows**

```bash
python -m venv venv

venv\Scripts\activate
```

**Linux**

```bash
python3 -m venv venv

source venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar migrações

```bash
python manage.py migrate
```

### Criar o superusuário inicial

O superusuário é o administrador do sistema, com acesso total e ao painel `/admin/`. Ele é necessário para os primeiros testes, por exemplo, para cadastrar os itens do cardápio.

```bash
python manage.py createsuperuser
```

O Django solicitará:

- **Username**: nome de login (ex.: `admin`);
- **Email address**: pode ser deixado em branco (Enter);
- **Password**: a senha não aparece enquanto é digitada; digite duas vezes para confirmar.

Se o Django informar que o usuário já existe, escolha outro nome.

### Executar o servidor

```bash
python manage.py runserver
```

Depois acesse:

http://127.0.0.1:8000/

### Endereços principais

| Endereço | Descrição |
|---|---|
| http://127.0.0.1:8000/accounts/login/ | Tela de login |
| http://127.0.0.1:8000/clientes/cadastro/ | Cadastro de novo cliente |
| http://127.0.0.1:8000/itens/ | Cardápio |
| http://127.0.0.1:8000/pedidos/ | Pedidos |
| http://127.0.0.1:8000/admin/ | Painel administrativo do Django |

### Roteiro rápido de teste

1. Entre com o superusuário em `/accounts/login/` e cadastre alguns itens em **Cardápio → Novo item**;
2. Saia do sistema e crie uma conta de cliente em `/clientes/cadastro/`;
3. Entre como cliente, abra o **Cardápio** e clique em **Itens do pedido** em um item; informe a quantidade e a observação e clique em **Salvar**;
4. Na tela do pedido, use **Adicionar mais itens** (se quiser) e clique em **Concluir pedido**;
5. Entre novamente com o superusuário e confira o pedido enviado em **Pedidos**.

### Executar os testes automatizados

```bash
python manage.py test
```

## Perfis de usuário

- **Cliente**: criado pela tela de cadastro; entra automaticamente no grupo "Cliente", que já recebe as permissões necessárias (ver o cardápio e fazer pedidos);
- **Gerente, Garçom e Cozinheiro**: cadastrados como funcionários; entram no grupo do cargo escolhido, e as permissões podem ser ajustadas no painel `/admin/`, em **Grupos**;
- **Superusuário**: acesso total ao sistema.

## Fundamentação

O desenvolvimento do sistema fundamenta-se na necessidade de organizar o atendimento em restaurantes, onde pedidos anotados manualmente estão sujeitos a erros de escrita, esquecimentos e cálculos incorretos de valores.

Ao permitir que o pedido seja montado no próprio sistema, com cálculo automático de valores e registro dos pedidos em ordem de horário, o Churrascaria PSW busca tornar o atendimento mais ágil, organizado e confiável.

## Autoria

Desenvolvimento do software:

**Sabrina Santana de Souza**

**Vinícius Pires Silveira**  
Turma 3AII — Curso Técnico em Informática para Internet — IF Baiano, Campus Guanambi-BA

## Licença

Projeto desenvolvido como atividade avaliativa do Curso Técnico em Informática para Internet.

