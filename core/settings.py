import os
from pathlib import Path
import dj_database_url

# 1. Environment Detection
IS_HEROKU = "RENDER" in os.environ

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l3q_pg_@*c9nk3#&+!0cu70b6i_85%0owotbu(jo^jf#nh7rp('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Auth Redirects
LOGIN_URL = 'login'              
LOGIN_REDIRECT_URL = 'home'      
LOGOUT_REDIRECT_URL = 'home'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be here for Render, but we skip it locally to keep images fast
    *(['whitenoise.middleware.WhiteNoiseMiddleware'] if IS_HEROKU else []),
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# 2. Database Configuration
if not IS_HEROKU:
    # LOCAL: Connects to your pgAdmin 'happy_heavens_db'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'happy_heavens_db',
            'USER': 'postgres',
            'PASSWORD': 'root123',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    # PRODUCTION: Connects to Render Cloud DB
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600
        )
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 3. Static & Media Configuration
STATIC_URL = 'static/'
# Where Render gathers files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Where your CSS and UI images live
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Production Storage (Only on Render)
if IS_HEROKU:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Product Images
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 4. Session Settings
SESSION_COOKIE_AGE = 604800 
SESSION_SAVE_EVERY_REQUEST = True