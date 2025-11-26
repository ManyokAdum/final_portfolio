# Fix for TypeError: issubclass() arg 1 must be a class

## Problem

You're seeing this error in Vercel logs:
```
TypeError: issubclass() arg 1 must be a class
File "/var/task/vc__handler__python.py", line 463
```

This error occurs in Vercel's internal handler code when it tries to introspect your handler function.

## Root Cause

Vercel's Python runtime tries to detect what type of handler you're using by inspecting the function and module. When Django initializes at module level, it can affect the module's namespace or function metadata in ways that confuse Vercel's introspection code.

The specific issue is that Vercel's runtime checks if your handler is a subclass of `BaseHTTPRequestHandler`, but during this check, it encounters something that's not a class (possibly `None` or a function object that got wrapped).

## Solution

The fix is to **delay all Django imports and initialization until inside the handler function**. This ensures:

1. The handler function is clean and simple when Vercel first inspects it
2. No module-level side effects from Django initialization
3. Vercel can properly detect the handler function type

## What Changed

**Before (Problematic):**
```python
# Django imports at module level - confuses Vercel
from django.core.wsgi import get_wsgi_application
django_app = get_wsgi_application()  # Module-level initialization

def handler(request):
    # Use django_app
    ...
```

**After (Fixed):**
```python
# No Django imports at module level
_django_app = None  # Lazy initialization

def handler(request):
    # Import and initialize Django inside handler
    global _django_app
    if _django_app is None:
        from django.core.wsgi import get_wsgi_application
        _django_app = get_wsgi_application()
    # Use _django_app
    ...
```

## Key Principles

1. **Keep handler function clean**: Vercel needs to inspect it before any complex initialization
2. **Lazy initialization**: Initialize Django only when the handler is actually called
3. **Minimal module-level code**: Only basic setup (paths, environment) at module level
4. **Cache the app**: Use a global variable to cache the Django app after first initialization

## Testing

After deploying this fix:

1. Check Vercel logs - the `TypeError: issubclass()` error should be gone
2. Test your homepage - it should load correctly
3. Test static files - CSS, JS, images should work
4. Monitor cold starts - first request might be slightly slower (normal for lazy initialization)

## Why This Works

- **Vercel's introspection happens at import time**: When Vercel loads your module, it inspects the handler function. If Django has already initialized, it might have modified the module namespace in ways that confuse Vercel's type checking.

- **Lazy loading defers side effects**: By moving Django initialization inside the handler, we ensure the module is "clean" when Vercel first inspects it. The handler function is just a simple function that Vercel can properly detect.

- **Caching prevents repeated initialization**: Using a global cache ensures we only initialize Django once, not on every request.

## Alternative Approaches (If This Doesn't Work)

If you still see issues:

1. **Check Python version**: Ensure you're using a compatible Python version (3.9+ recommended)

2. **Simplify further**: Try removing even more module-level code

3. **Check dependencies**: Some packages might have compatibility issues with Vercel's runtime

4. **Consider different deployment**: If Django on Vercel continues to be problematic, consider:
   - Railway or Render (better Django support)
   - AWS Lambda with Zappa or Mangum
   - Traditional hosting (Heroku, DigitalOcean)

## Related Errors

If you see similar errors:
- `AttributeError` during handler detection
- `TypeError` related to class checking
- Handler not being found

These are all related to Vercel's runtime trying to introspect your code. The solution is the same: keep the handler function and module-level code as simple as possible.

