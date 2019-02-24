from django.apps import AppConfig


class QuackConfig(AppConfig):
    name = 'quack'

    def ready(self):
        import quack.signals
