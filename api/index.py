"""
Vercel serverless function entry point for Django
"""
import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Set environment variable to indicate we're on Vercel
os.environ['VERCEL'] = '1'

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

# Import and initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
django_app = get_wsgi_application()

def handler(req, res):
    """
    Vercel serverless function handler for Django
    """
    from io import BytesIO
    
    # Get request details
    method = getattr(req, 'method', 'GET')
    url = getattr(req, 'url', '/')
    path = getattr(req, 'path', '/')
    query = getattr(req, 'query', {})
    headers = getattr(req, 'headers', {})
    body = getattr(req, 'body', b'')
    
    # Handle query string
    if isinstance(query, dict):
        query_string = '&'.join([f'{k}={v}' for k, v in query.items()])
    else:
        query_string = str(query)
    
    # Convert body to bytes
    if isinstance(body, str):
        body = body.encode('utf-8')
    elif body is None:
        body = b''
    
    # Build WSGI environ
    host = headers.get('host', 'localhost') if isinstance(headers, dict) else 'localhost'
    scheme = headers.get('x-forwarded-proto', 'https') if isinstance(headers, dict) else 'https'
    
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'SCRIPT_NAME': '',
        'CONTENT_TYPE': headers.get('content-type', '') if isinstance(headers, dict) else '',
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
    
    # Add HTTP headers
    if isinstance(headers, dict):
        for key, value in headers.items():
            key_upper = key.upper().replace('-', '_')
            if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH', 'HOST'):
                environ[f'HTTP_{key_upper}'] = value
    
    # Response containers
    status = [200]
    headers_list = []
    
    def start_response(status_line, headers):
        status[0] = int(status_line.split()[0])
        headers_list[:] = headers
    
    # Process through Django
    try:
        response_body = django_app(environ, start_response)
        body_content = b''.join(response_body).decode('utf-8', errors='ignore')
        
        # Set response using Vercel's res object
        res.status(status[0])
        for key, value in headers_list:
            res.headers[key] = value
        res.send(body_content)
        
    except Exception as e:
        import traceback
        error_msg = f'Error: {str(e)}\n{traceback.format_exc()}'
        res.status(500)
        res.headers['Content-Type'] = 'text/plain'
        res.send(error_msg)
