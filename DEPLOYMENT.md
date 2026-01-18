# Deployment Guide for Render

This guide will help you deploy the Employee Management System to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Git repository with your code

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub/GitLab/Bitbucket
2. In Render dashboard, click "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and configure everything
5. Set the following environment variables in Render dashboard:
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com` (Render will provide this)
   - `SECRET_KEY`: Generate a strong secret key (Render can auto-generate this)

### Option 2: Manual Setup

1. **Create a Web Service:**
   - In Render dashboard, click "New" → "Web Service"
   - Connect your repository
   - Set the following:
     - **Name**: employee-management (or your preferred name)
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - **Start Command**: `gunicorn employee_management.wsgi:application`

2. **Create a PostgreSQL Database:**
   - In Render dashboard, click "New" → "PostgreSQL"
   - Choose a name and plan
   - Note the connection details

3. **Set Environment Variables:**
   In your Web Service settings, add these environment variables:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a strong secret key (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `ALLOWED_HOSTS`: `your-app-name.onrender.com`
   - `DATABASE_URL`: (Automatically set by Render if you linked the database)

4. **Link Database to Web Service:**
   - In your Web Service settings, go to "Connections"
   - Link your PostgreSQL database
   - Render will automatically set `DATABASE_URL`

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Set to `False` in production | `False` |
| `SECRET_KEY` | Django secret key | Auto-generated or custom |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `your-app.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection URL | Auto-set by Render |
| `SECURE_SSL_REDIRECT` | Force HTTPS (optional) | `True` |

## Post-Deployment

1. **Create Superuser:**
   - Go to Render dashboard → Your Web Service → Shell
   - Run: `python manage.py createsuperuser`
   - Follow the prompts

2. **Access Your Application:**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - Admin panel: `https://your-app-name.onrender.com/admin/`

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` runs during build
- Check that `STATIC_ROOT` is set correctly
- Verify WhiteNoise middleware is in `MIDDLEWARE`

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check database is linked to web service
- Ensure `dj-database-url` is in requirements.txt

### 500 Errors
- Check Render logs for detailed error messages
- Verify all environment variables are set
- Ensure `ALLOWED_HOSTS` includes your Render domain

## Local Development

To run locally with the same setup:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables (create `.env` file):
   ```
   DEBUG=True
   SECRET_KEY=your-local-secret-key
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Run server:
   ```bash
   python manage.py runserver
   ```

## Notes

- The application uses SQLite locally and PostgreSQL on Render
- Static files are served via WhiteNoise middleware
- Database migrations run automatically during build
- All security settings are enabled when `DEBUG=False`

