"""
Django settings for recoverit project.
"""
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# -----------------------------------------------------------------------
# Environment variables (django-environ reads from a .env file)
# -----------------------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env('SECRET_KEY')
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cloudinary_storage',
    'cloudinary',

    # Local apps
    'accounts',
    'dashboard',
    'lostfound',
]
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default=''),
    'API_KEY': env('CLOUDINARY_API_KEY', default=''),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default=''),
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
ROOT_URLCONF = 'recoverit.urls'

STORAGES ={
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    "staticfiles":{
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
             },
    }

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
            ],
        },
    },
]

WSGI_APPLICATION = 'recoverit.wsgi.application'


# -----------------------------------------------------------------------
# Database — Supabase PostgreSQL, configured via environment variables
# -----------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', default='5432'),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Auth backends / login-logout redirects
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'accounts:login'


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------
# Static files
# -----------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# -----------------------------------------------------------------------
# Media files (user uploads)
# -----------------------------------------------------------------------
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'