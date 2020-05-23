"""
Django settings for TinyDevCRM.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
#
# NOTE: bool('0') is True because string is non-empty, convert to int for proper
# mapping instead.
DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split()


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django REST Framework
    'rest_framework',
    # 'SimpleJWT' does not need to be added to INSTALLED_APPS.
    # Addressing CORS failures
    'corsheaders',
    # DRF SimpleJWT token blacklist for BlacklistMixin
    'rest_framework_simplejwt.token_blacklist',

    # Authentication service #
    'authentication',
    # Tables service #
    'tables',
    # Views service #
    'views',
    # Jobs service #
    'jobs',
    # Events service #
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS middleware; I think from the README Django middleware ordering is
    # important, and must come before
    # 'django.middleware.common.CommonMiddleware'
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = (
    'wsgi.application'
    if DEBUG
    else
    'src.core.wsgi.application'
)


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get(
            'SQL_ENGINE',
            'django.db.backends.sqlite3'
        ),
        'NAME': os.environ.get(
            'SQL_DATABASE',
            os.path.join(
                BASE_DIR,
                'db.sqlite3'
            )
        ),
        'USER': os.environ.get(
            'SQL_USER',
            'user'
        ),
        'PASSWORD': os.environ.get(
            'SQL_PASSWORD',
            'password'
        ),
        'HOST': os.environ.get(
            'SQL_HOST',
            'localhost'
        ),
        'PORT': os.environ.get(
            'SQL_PORT',
            '5432'
        )
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model for JSON Web Token authentication
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
AUTH_USER_MODEL = 'authentication.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Django REST Framework settings #
REST_FRAMEWORK = {
    # Tuples must have commas to separate values, otherwise will resolve to
    # strings: https://stackoverflow.com/a/53377480/1497211
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.authentication.JWTAuthentication',
    )
}


# Django REST Framework SimpleJWT settings #
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    # Others have also used 'Bearer' as a common JWT auth header.
    'AUTH_HEADER_TYPES': ('JWT'),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
    'TOKEN_TYPE_CLAIM': 'token_type'
}


# CORS settings.
CORS_ORIGIN_WHITELIST = [
    'https://dashboard.tinydevcrm.com',
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get(
    'STATIC_ROOT',
    '/public/static'
)


# Media files (CSV data dumps, PostgreSQL stored procedures, etc.)
# https://docs.djangoproject.com/en/3.0/topics/files/
# https://learndjango.com/tutorials/django-file-and-image-uploads-tutorial
MEDIA_ROOT = os.environ.get(
    'MEDIA_ROOT',
    '/tinydevcrm-files'
)
