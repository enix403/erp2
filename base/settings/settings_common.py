"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = 'rj@xxwc_h@fhvnu7%uzgteh$5pbrc4vqf8(z8r9c=$qebd!7!y'
ALLOWED_HOSTS = ['*']

DEBUG = os.getenv('APP_DEBUG') == 'true'

ROOT_URLCONF = 'base.urls'
WSGI_APPLICATION = 'base.wsgi.application'


INSTALLED_APPS = [
    'salary.apps.SalaryConfig',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'salary.middlewares.midrouter.RouterMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    #! NOTE: make sure to read django-htmlmin docs if you
    #! plan to enable django caching system
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],

        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.getenv('DB_USER', 'root'),
        'NAME': os.getenv('DB_NAME', ''),
        'PASSWORD': os.getenv('DB_PASS', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MESSAGE_LEVEL = 0

SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = BASE_DIR / 'storage/sessions'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

INTERNAL_IPS = [
    '127.0.0.1',
]

