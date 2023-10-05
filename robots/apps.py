from django.apps import AppConfig


class RobotsConfig(AppConfig):
    name = 'robots'

    def ready(sels):
        import robots.signals  # noqa: F401
