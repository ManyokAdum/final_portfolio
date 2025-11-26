"""
Vercel serverless function entry point for Django
"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set environment variable to indicate we're on Vercel
os.environ['VERCEL'] = '1'

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Import and initialize Django WSGI application
try:
    from django.core.wsgi import get_wsgi_application
    django_app = get_wsgi_application()
except Exception as e:
    # If Django initialization fails, we'll handle it in the handler
    django_app = None
    init_error = str(e)

def handler(request):
    """
    Vercel serverless function handler for Django
    
    This function adapts Vercel's Request/Response API to Django's WSGI interface.
    """
    # Check if Django app initialized successfully
    if django_app is None:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Django initialization error: {init_error}'
        }
    
    try:
        # Extract request information
        # Vercel's Request object structure may vary, so we handle multiple cases
        method = getattr(request, 'method', 'GET')
        
        # Get path - handle both 'path' and 'url' attributes
        if hasattr(request, 'path'):
            path = request.path
        elif hasattr(request, 'url'):
            # Extract path from URL
            url = request.url
            if '?' in url:
                path = url.split('?')[0]
            else:
                path = url
        else:
            path = '/'
        
        # Get query string
        if hasattr(request, 'query_string'):
            query_string = request.query_string or ''
        elif hasattr(request, 'query'):
            query = request.query or {}
            if isinstance(query, dict):
                query_string = '&'.join([f'{k}={v}' for k, v in query.items()])
            else:
                query_string = str(query)
        else:
            query_string = ''
        
        # Get headers
        if hasattr(request, 'headers'):
            headers = dict(request.headers) if request.headers else {}
        else:
            headers = {}
        
        # Get request body
        body = b''
        if hasattr(request, 'body'):
            body_data = request.body
            if isinstance(body_data, str):
                body = body_data.encode('utf-8')
            elif isinstance(body_data, bytes):
                body = body_data
            elif body_data is not None:
                body = str(body_data).encode('utf-8')
        
        # Build WSGI environ dictionary
        host = headers.get('host', 'localhost')
        scheme = headers.get('x-forwarded-proto', 'https')
        
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'SCRIPT_NAME': '',
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)),
            'SERVER_NAME': host.split(':')[0] if ':' in host else host,
            'SERVER_PORT': host.split(':')[1] if ':' in host else '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': scheme,
            'wsgi.input': BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers to environ
        for key, value in headers.items():
            key_upper = key.upper().replace('-', '_')
            if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HOST'):
                environ[f'HTTP_{key_upper}'] = value
        
        # Response containers for WSGI start_response callback
        status_code = [200]
        response_headers = []
        
        def start_response(status_line, headers):
            status_code[0] = int(status_line.split()[0])
            response_headers[:] = headers
        
        # Process request through Django WSGI application
        response_body = django_app(environ, start_response)
        body_content = b''.join(response_body).decode('utf-8', errors='ignore')
        
        # Convert WSGI headers to dict
        headers_dict = dict(response_headers)
        
        # Return response in Vercel's expected format
        # Try to use Response object if available, otherwise return dict
        try:
            from vercel import Response
            return Response(
                body_content,
                status=status_code[0],
                headers=headers_dict
            )
        except ImportError:
            # Fallback: return dict format (some Vercel runtimes accept this)
            return {
                'statusCode': status_code[0],
                'headers': headers_dict,
                'body': body_content
            }
        
    except Exception as e:
        import traceback
        error_msg = f'Error: {str(e)}\n{traceback.format_exc()}'
        
        # Try to return proper Response object, otherwise use dict
        try:
            from vercel import Response
            return Response(
                error_msg,
                status=500,
                headers={'Content-Type': 'text/plain'}
            )
        except ImportError:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'text/plain'},
                'body': error_msg
            }
