# Deploying Django Portfolio to Render

This guide will help you deploy your Django portfolio application to Render.

## Prerequisites

- A Render account (sign up at https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Create a PostgreSQL Database (Optional but Recommended)

1. Go to your Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name**: `portfolio-db` (or your preferred name)
   - **Database**: `portfolio`
   - **User**: Auto-generated
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: Latest stable
   - **Plan**: Free tier is fine for development
4. Click "Create Database"
5. **Save the Internal Database URL** - you'll need this later

## Step 2: Create a Web Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your Git repository
3. Configure the service:

   **Basic Settings:**
   - **Name**: `portfolio` (or your preferred name)
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `portfolio` if your Django project is in a subdirectory)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     gunicorn portfolio.wsgi:application
     ```

   **Advanced Settings:**
   - **Auto-Deploy**: Yes (deploys on every push to main branch)

## Step 3: Set Environment Variables

In your Web Service settings, go to "Environment" and add:

1. **SECRET_KEY**: 
   - Generate a new secret key:
     ```python
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Or use: https://djecrety.ir/

2. **DEBUG**: `False` (for production)

3. **DATABASE_URL**: 
   - If you created a PostgreSQL database, use the **Internal Database URL** from your database service
   - Format: `postgresql://user:password@hostname:port/database`
   - If you want to use SQLite (not recommended for production), you can skip this

4. **RENDER_EXTERNAL_HOSTNAME**: 
   - This is automatically set by Render, but you can also manually set it to your service URL
   - Format: `your-app-name.onrender.com`

## Step 4: Deploy

1. Click "Create Web Service"
2. Render will:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Run `collectstatic` to gather static files
   - Start your application with Gunicorn

3. Wait for the build to complete (usually 2-5 minutes)

4. Once deployed, your site will be available at: `https://your-app-name.onrender.com`

## Step 5: Run Migrations (First Time)

After the first deployment, you need to run database migrations:

1. Go to your Web Service dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py migrate
   ```

Or you can add this to your build command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

## Troubleshooting

### Build Fails

- **Check logs**: Go to your service → "Logs" tab
- **Common issues**:
  - Missing dependencies in `requirements.txt`
  - Wrong Python version (Render auto-detects, but you can specify in `runtime.txt`)
  - Build command errors

### Static Files Not Loading

- Ensure `whitenoise` is in `requirements.txt` ✅ (already included)
- Check that `collectstatic` runs during build
- Verify `STATIC_ROOT` is set correctly in `settings.py` ✅ (already configured)

### Database Connection Issues

- Verify `DATABASE_URL` environment variable is set correctly
- Check that your database service is running
- Ensure you're using the **Internal Database URL** (not External)
- If using PostgreSQL, ensure `psycopg2` is in `requirements.txt` ✅ (already included)

### 500 Errors

- Check application logs in Render dashboard
- Verify `DEBUG=False` and `SECRET_KEY` is set
- Ensure `ALLOWED_HOSTS` includes your Render domain
- Check that migrations have been run

## Environment Variables Summary

Make sure these are set in your Render Web Service:

| Variable | Value | Required |
|----------|-------|----------|
| `SECRET_KEY` | Your Django secret key | ✅ Yes |
| `DEBUG` | `False` | ✅ Yes |
| `DATABASE_URL` | PostgreSQL connection string | ⚠️ Recommended |
| `RENDER_EXTERNAL_HOSTNAME` | Auto-set by Render | ✅ Auto |

## File Structure

Your project should have:
```
portfolio/
├── manage.py
├── requirements.txt          ✅ (already exists)
├── build.sh                  ✅ (already exists)
├── portfolio/
│   ├── settings.py           ✅ (configured for Render)
│   ├── wsgi.py
│   └── ...
└── ...
```

## Additional Notes

- **Free Tier Limitations**: 
  - Services spin down after 15 minutes of inactivity
  - First request after spin-down may take 30-60 seconds
  - Consider upgrading to paid plan for always-on service

- **Custom Domain**: 
  - You can add a custom domain in Render dashboard
  - Update `ALLOWED_HOSTS` in settings.py to include your domain

- **Monitoring**: 
  - Render provides basic metrics and logs
  - Check "Metrics" and "Logs" tabs in your service dashboard

## Support

- Render Documentation: https://render.com/docs
- Django Deployment Checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

