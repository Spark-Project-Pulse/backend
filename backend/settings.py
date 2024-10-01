# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

import os
from pathlib import Path

# Check to see if the environment is set to production (K_SERVICE is a Google Cloud Run environment variable)
if os.getenv('K_SERVICE'):
    from .production import *
else:
    # for local docker and django development
    from .development import *
    
# Base settings shared by all environments below

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

# Supabase keys
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Useful for managing database via a web interface
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # 'django.contrib.contenttypes',  
    # 'django.contrib.auth',
    'corsheaders',
]

# Security settings
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware', #SHOULD PROLLY ENABLE LATER MUST DISCUSS
    # 'django.contrib.auth.middleware.AuthenticationMiddleware', # Useful for managing database via a web interface
]

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'

# Internationalization (https://docs.djangoproject.com/en/5.0/topics/i18n/)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type (https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'