from django.apps import AppConfig

class MainappConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        pass
        # from scheduler import scheduler
        # scheduler.start()

    