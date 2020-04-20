from django.apps import AppConfig


class ClienteConfig(AppConfig):
    name = 'cliente'

    def ready(self):
    	import cliente.signals
