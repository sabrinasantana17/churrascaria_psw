from django.apps import AppConfig


class ClienteConfig(AppConfig):
    name = 'cliente'

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from .grupo import garantir_grupo_ao_logar
        user_logged_in.connect(garantir_grupo_ao_logar)
