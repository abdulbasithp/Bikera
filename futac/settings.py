"""
Django settings for futac project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from email.policy import default
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['65.1.86.255']
STATIC_ROOT = '/var/www/mysite/assets/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'user',
    'superadmin',
    'cart',
    'order',
    'storages',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'futac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.views.categories' ,
                'store.views.brands', 
                'cart.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'futac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),
        'NAME': config('NAME'),
        'USER' : config('USER'),
        'PASSWORD' : config('PASSWORD'),
        'HOST': config('HOST'),
        'POST': config('POST') ,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [ 
        os.path.join(BASE_DIR, "static")
        ]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'static/images/media')

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AUTH_USER_MODEL = 'user.Account'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email SMTP
EMAIL_BACKEND       = config('EMAIL_BACKEND')
EMAIL_HOST          = config('EMAIL_HOST')
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT          = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS       = config('EMAIL_USE_TLS', default=True, cast=bool)


# password hashers
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


# paytm marchant ids 

PAYTM_MERCHANT_ID = config('PAYTM_MERCHANT_ID')
PAYTM_SECRET_KEY = config('PAYTM_SECRET_KEY')
PAYTM_WEBSITE = config('PAYTM_WEBSITE')
PAYTM_CHANNEL_ID = config('PAYTM_CHANNEL_ID')
PAYTM_INDUSTRY_TYPE_ID = config('PAYTM_INDUSTRY_TYPE_ID')

# aws s3 bucket 
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = config('AWS_QUERYSTRING_AUTH', default=True, cast=bool)
AWS_S3_FILE_OVERWRITE = config('AWS_S3_FILE_OVERWRITE', default=True, cast=bool)