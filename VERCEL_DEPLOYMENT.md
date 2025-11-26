# Vercel Deployment Guide

This guide explains how to deploy your Django portfolio to Vercel.

## Files Created/Modified

1. **`vercel.json`** - Vercel configuration file that routes all requests to the Django app
2. **`api/index.py`** - Serverless function handler that bridges Vercel's runtime with Django's WSGI
3. **`portfolio/settings.py`** - Updated to handle Vercel environment
4. **`.vercelignore`** - Excludes unnecessary files from deployment

## Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

   Or for production:
   ```bash
   vercel --prod
   ```

## Important Notes

- **Static Files**: Static files are served through Django. Make sure your static files are in `portfolio/core/static/`
- **Database**: SQLite is used by default. For production, consider using a managed database service.
- **Environment Variables**: If you need to set environment variables, use Vercel's dashboard or CLI:
  ```bash
  vercel env add SECRET_KEY
  ```

## Troubleshooting

If you encounter a 404 error:
1. Make sure `api/index.py` exists and is in the correct location
2. Verify that `vercel.json` is in the project root
3. Check that all routes in `vercel.json` point to `/api/index.py`
4. Ensure `PYTHONPATH` is set correctly in `vercel.json`

## Project Structure

```
portfolio/
├── api/
│   └── index.py          # Vercel serverless function
├── portfolio/
│   ├── core/
│   │   ├── static/       # Static files (CSS, JS, Images)
│   │   └── templates/    # HTML templates
│   ├── settings.py       # Django settings (updated for Vercel)
│   └── urls.py
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── manage.py
```

