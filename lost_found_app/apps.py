from django.apps import AppConfig

class LostFoundAppConfig(AppConfig):
    name = 'lost_found_app'

    def ready(self):
        import lost_found_app.signals