from django.apps import AppConfig

class DailyReportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_report'

    def ready(self):
        import daily_report.signals
