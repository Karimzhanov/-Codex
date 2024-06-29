from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Set CORS headers
        response['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow specific HTTP methods
        response['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow specific headers
        
        # Determine Cross-Origin-Resource-Policy based on origin check
        if is_same_origin(request.build_absolute_uri()):
            response['Cross-Origin-Resource-Policy'] = 'same-site'  # или 'cross-origin', в зависимости от вашего случая
        else:
            response['Cross-Origin-Resource-Policy'] = 'cross-origin'

        return response

def is_same_origin(url):
    # Example function to check if the URL is of the same origin
    return 'instagram.com' in url
