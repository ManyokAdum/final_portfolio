"""
Vercel serverless function entry point for Django
All Django imports are done inside the handler to avoid confusing Vercel's runtime introspection
"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Minimal setup - no Django imports at module level
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Environment setup
os.environ['VERCEL'] = '1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Global cache for Django app
_django_app = None
_django_error = None

def handler(request):
    """
    Vercel serverless function handler
    
    Keep this function completely clean - all Django code is inside
    to prevent Vercel's runtime from getting confused during introspection.
    """
    global _django_app, _django_error
    
    # Initialize Django app on first call (lazy loading)
    if _django_app is None and _django_error is None:
        try:
            from django.core.wsgi import get_wsgi_application
            _django_app = get_wsgi_application()
        except Exception as e:
            import traceback
            _django_error = {
                'message': str(e),
                'traceback': traceback.format_exc()
            }
    
    # Return error if initialization failed
    if _django_error:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f"Django Initialization Error:\n{_django_error['message']}\n\n{_django_error['traceback']}"
        }
    
    try:
        # Extract request data
        method = getattr(request, 'method', 'GET')
        
        # Get path
        path = getattr(request, 'path', None)
        if not path:
            url = getattr(request, 'url', '/')
            path = url.split('?')[0] if '?' in url else url
        
        # Get query string
        query_string = ''
        if hasattr(request, 'query_string'):
            query_string = request.query_string or ''
        elif hasattr(request, 'query'):
            q = getattr(request, 'query', {})
            if isinstance(q, dict):
                query_string = '&'.join(f'{k}={v}' for k, v in q.items() if v)
            elif q:
                query_string = str(q)
        
        # Get headers
        headers = {}
        if hasattr(request, 'headers'):
            h = request.headers
            if h:
                headers = dict(h) if not isinstance(h, dict) else h
        
        # Get body
        body = b''
        if hasattr(request, 'body'):
            b = request.body
            if isinstance(b, str):
                body = b.encode('utf-8')
            elif isinstance(b, bytes):
                body = b
            elif b is not None:
                body = str(b).encode('utf-8')
        
        # Build WSGI environ
        host = headers.get('host', 'localhost')
        scheme = headers.get('x-forwarded-proto', 'https')
        
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'SCRIPT_NAME': '',
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': host.split(':')[0],
            'SERVER_PORT': host.split(':')[1] if ':' in host else '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': scheme,
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers
        for key, value in headers.items():
            env_key = key.upper().replace('-', '_')
            if env_key not in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HOST'):
                environ[f'HTTP_{env_key}'] = value
        
        # WSGI response
        status_code = [200]
        response_headers = []
        
        def start_response(status_line, headers_list):
            status_code[0] = int(status_line.split()[0])
            response_headers[:] = headers_list
        
        # Call Django
        response_iter = _django_app(environ, start_response)
        response_body = b''.join(response_iter)
        
        # Decode response
        try:
            body_text = response_body.decode('utf-8')
        except UnicodeDecodeError:
            body_text = response_body.decode('utf-8', errors='replace')
        
        # Return Vercel response
        return {
            'statusCode': status_code[0],
            'headers': dict(response_headers),
            'body': body_text
        }
        
    except Exception as e:
        import traceback
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain; charset=utf-8'},
            'body': f"Request Processing Error:\n{str(e)}\n\n{traceback.format_exc()}"
        }
