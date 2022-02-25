from django.apps import AppConfig




class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company'
    
    
    def ready(self):
        from company.aps_scheduler import start
        print('Ready function working')
        start()