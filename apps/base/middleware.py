from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Разрешаем доступ с любого домена
        response['Access-Control-Allow-Origin'] = '*'
        
        return response