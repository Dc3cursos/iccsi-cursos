from django.core.wsgi import get_wsgi_application
import os

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iccsi.iccsi.settings')
application = get_wsgi_application()

def handler(request):
    return application(request)
