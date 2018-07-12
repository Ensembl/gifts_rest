"""
Django settings for gifts_rest project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from . import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Custom User model for the service
AUTH_USER_MODEL = 'aap_auth.AAPUser'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

TIME_ZONE = 'Europe/London'
USE_TZ = True

# SECURITY WARNING: don't run with debug turned on in production!
if env.PROD_ENV:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django.contrib.postgres',
    'psqlextra',
    'restui',
    'aap_auth.apps.AppAuthConfig'
]

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'aap_auth.backend.AAPBackend',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gifts_rest.urls'

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

WSGI_APPLICATION = 'gifts_rest.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if 'TRAVIS' in os.environ:
    SECRET_KEY = "SecretKeyForUseOnTravis"
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisci',
            'USER':     'travis',
#            'PASSWORD': '',
            'HOST':     '127.0.0.1',
#            'PORT':     '',
        },
        'gifts': {
            'ENGINE':   'psqlextra.backend',
            'NAME':     'travisci',
            'USER':     'travis',
#            'PASSWORD': '',
            'HOST':     '127.0.0.1',
#            'PORT':     '',
        }
    }
else:
    from . import secrets
    SECRET_KEY = secrets.SECRET_KEY
    DATABASES = {
        'default': {
            'ENGINE': 'psqlextra.backend', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'OPTIONS': {
                'options': '-c search_path=ensembl_gifts,public'
            },
            'NAME': secrets.GIFTS_DATABASE,
            'USER': secrets.GIFTS_DATABASE_USER,
            'PASSWORD': secrets.GIFTS_DATABASE_PASSWORD,
            'HOST': secrets.GIFTS_DATABASE_HOST,
            'PORT': secrets.GIFTS_DATABASE_PORT,
#             'NAME': secrets.REST_DATABASE,
#             'USER': secrets.REST_DATABASE_USER,
#             'PASSWORD': secrets.REST_DATABASE_PASSWORD,
#             'HOST': secrets.REST_DATABASE_HOST,                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
#             'PORT': secrets.REST_DATABASE_PORT,                      # Set to empty string for default.
        },
        'gifts': {
            'ENGINE': 'psqlextra.backend',
            'OPTIONS': {
                'options': '-c search_path=ensembl_gifts,public'
            },
            'NAME': secrets.GIFTS_DATABASE,
            'USER': secrets.GIFTS_DATABASE_USER,
            'PASSWORD': secrets.GIFTS_DATABASE_PASSWORD,
            'HOST': secrets.GIFTS_DATABASE_HOST,
            'PORT': secrets.GIFTS_DATABASE_PORT,
        }
    }

DATABASE_ROUTERS = ['gifts_rest.router.GiftsRouter']

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# TaRK base URL
TARK_SERVER = "http://betatark.ensembl.org"

# AAP service
AAP_PEM_URL = 'https://explore.api.aai.ebi.ac.uk/meta/public.pem'
AAP_PROFILE_URL = 'https://explore.api.aai.ebi.ac.uk/users/{}/profile'
AAP_PEM_FILE = '/tmp/aap.pem'

