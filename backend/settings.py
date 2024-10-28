# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

import os
from pathlib import Path
from services.secret_manager import get_secret

# Check if the environment is set to production (K_SERVICE is a Google Cloud Run environment variable)
IS_PRODUCTION = bool(os.getenv('K_SERVICE'))

if IS_PRODUCTION:
    from .production import *
else:
    # for local docker and django development
    from .development import *

# Base settings shared by all environments below

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_secret('SECRET_KEY')

# Supabase keys
SUPABASE_NAME=get_secret('SUPABASE_NAME')
SUPABASE_USER=get_secret('SUPABASE_USER')
SUPABASE_PASSWORD=get_secret('SUPABASE_PASSWORD')
SUPABASE_HOST=get_secret('SUPABASE_HOST')
SUPABASE_PORT=get_secret('SUPABASE_PORT')
SUPABASE_URL=get_secret('SUPABASE_URL')
SUPABASE_ANON_KEY=get_secret('SUPABASE_ANON_KEY')

INSTALLED_APPS = [
    'django.contrib.contenttypes', 
    'django.contrib.auth', # TODO: eventually check if we can remove this
    'corsheaders',
    'pulse',
    'rest_framework',
]

# Security settings (NOTE: order DOES matter)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware', # Useful for managing database via a web interface
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SUPABASE_NAME,
        'USER': SUPABASE_USER,
        'PASSWORD': SUPABASE_PASSWORD,
        'HOST': SUPABASE_HOST,
        'PORT': SUPABASE_PORT,
        'OPTIONS': {
            'sslmode': DATABASE_OPTIONS_SSLMODE
        },
    }
}

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

# Internationalization (https://docs.djangoproject.com/en/5.0/topics/i18n/)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type (https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'