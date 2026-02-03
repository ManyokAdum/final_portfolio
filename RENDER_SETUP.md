# Render Deployment Setup - Quick Reference

## ✅ Files Updated

1. **render.yaml** - Created with proper Django configuration
2. **build.sh** - Updated to include migrations and dependencies

## 🚀 Deploying to Render

### Option 1: Using render.yaml (Recommended)

Render will automatically detect the `render.yaml` file and use those settings.

1. **Connect your GitHub repository** to Render
2. **Select the repository**: `ManyokAdum/final_portfolio`
3. **Render will automatically**:
   - Detect `render.yaml`
   - Use the correct build and start commands
   - Set up the service

### Option 2: Manual Configuration

If you prefer manual setup:

1. **Create a Web Service** on Render
2. **Configure these settings**:

   ```
   Name: final-portfolio
   Environment: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT
   ```

## 🔑 Required Environment Variables

Set these in Render Dashboard → Environment:

| Variable | Value | How to Set |
|----------|-------|------------|
| `SECRET_KEY` | Django secret key | Generate at https://djecrety.ir/ |
| `DEBUG` | `False` | Manual |
| `DATABASE_URL` | PostgreSQL URL | Optional - use if you create a database |
| `RENDER_EXTERNAL_HOSTNAME` | Auto-generated | Render sets this automatically |

## 📝 Step-by-Step Process

### 1. Create PostgreSQL Database (Optional but Recommended)

```
Dashboard → New → PostgreSQL
Name: final-portfolio-db
Plan: Free
```

Save the **Internal Database URL** for the next step.

### 2. Create Web Service

```
Dashboard → New → Web Service
Repository: ManyokAdum/final_portfolio
Branch: main
```

Render will auto-detect `render.yaml` and configure everything automatically!

### 3. Set Environment Variables

```
SECRET_KEY = [generate from https://djecrety.ir/]
DEBUG = False
DATABASE_URL = [your PostgreSQL Internal URL from step 1]
```

### 4. Deploy

Click **"Create Web Service"** - Render will:
- ✅ Install dependencies
- ✅ Collect static files
- ✅ Run migrations
- ✅ Start your app with Gunicorn

### 5. Access Your Site

Your portfolio will be live at:
```
https://final-portfolio.onrender.com
```

## 🐛 Troubleshooting

### Common Issues Fixed

✅ **"No module named 'app'"** - FIXED!
   - Was using: `gunicorn app:app` (Flask)
   - Now using: `gunicorn portfolio.wsgi:application` (Django)

✅ **Static files not loading** - FIXED!
   - WhiteNoise configured in settings.py
   - collectstatic runs during build

✅ **Database migrations** - FIXED!
   - Migrations run automatically in build.sh

### If Build Still Fails

1. **Check Logs** in Render Dashboard
2. **Verify** all environment variables are set
3. **Ensure** the latest code is pushed to GitHub:
   ```bash
   git status
   git push origin main
   ```

## 📱 Test Locally First

Before deploying, test locally:

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Test with Gunicorn
gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
```

Visit: http://localhost:8000

## 🎉 Success Checklist

- ✅ Code pushed to GitHub
- ✅ render.yaml created
- ✅ build.sh updated
- ✅ Environment variables configured
- ✅ Database created (optional)
- ✅ Deployment successful

---

**Your portfolio is now ready for deployment!** 🚀

Any changes you push to `main` branch will automatically redeploy.


