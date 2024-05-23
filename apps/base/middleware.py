# middleware.py
from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Добавляем заголовок Access-Control-Allow-Origin для разрешения доступа к ресурсам с других доменов
        response['Access-Control-Allow-Origin'] = 'https://example.com'
        
        return response
