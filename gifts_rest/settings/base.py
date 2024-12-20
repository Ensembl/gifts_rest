"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from datetime import timedelta

"""
Django settings for gifts_rest project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from . import secrets


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Custom User model for the service
AUTH_USER_MODEL = 'users.CustomUser'

API_VERSION = '1.0.0'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

TIME_ZONE = 'Europe/London'
USE_TZ = True


DEBUG = secrets.DEBUG
ALLOWED_HOSTS = secrets.ALLOWED_HOSTS
SECRET_KEY = secrets.SECRET_KEY
EMAIL_HOST = secrets.MAIL_SERVER
EMAIL_RECIPIENT_LIST = secrets.EMAIL_LIST
IS_FALLBACK = secrets.IS_FALLBACK

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'django.contrib.postgres',
    'psqlextra',
    'restui',
    'users.apps.UsersConfig'
]

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
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

if DEBUG is True:
    INSTALLED_APPS += ('corsheaders', )
    MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware' )
#    CORS_ORIGIN_ALLOW_ALL = DEBUG

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:39093',
    'localhost:8000',
)

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

DATABASES = {
    'default': {
        'ENGINE': 'psqlextra.backend',
        'OPTIONS': {
            'options': '-c search_path={}'.format(secrets.GIFTS_DATABASE_SCHEMA)
        },
        'NAME': secrets.GIFTS_DATABASE,
        'USER': secrets.GIFTS_DATABASE_USER,
        'PASSWORD': secrets.GIFTS_DATABASE_PASSWORD,
        'HOST': secrets.GIFTS_DATABASE_HOST,
        'PORT': secrets.GIFTS_DATABASE_PORT
    },
    # all operations on restui models point to 'gifts', see gifts_rest.router
    'gifts': {
        'ENGINE': 'psqlextra.backend',
        'OPTIONS': {
            'options': '-c search_path={},public'.format(secrets.GIFTS_DATABASE_SCHEMA)
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

STATIC_URL = '/gifts/api-static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/apache")


# TaRK base URL
TARK_SERVER = "http://tark.ensembl.org"

# Ensembl REST server
ENSEMBL_REST_SERVER = "http://rest.ensembl.org"

# CELERY STUFF
BROKER_URL = secrets.BROKER_URL
CELERY_RESULT_BACKEND = secrets.CELERY_RESULT_BACKEND
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {},
    "DOC_EXPANSION": None,
    "VALIDATOR_URL": None
}