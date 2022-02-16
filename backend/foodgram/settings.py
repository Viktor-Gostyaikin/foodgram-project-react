''' Project django settings. '''

import os

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'SECRET_KEY')

DEBUG = bool(os.environ.get('DEBUG'))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(', ')

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'api',
    'users',
    'recipes',
    'django_filters',
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

ROOT_URLCONF = 'foodgram.urls'

DOCS_DIR = os.path.join(BASE_DIR, 'api/docs/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [DOCS_DIR, ],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default="django.db.backends.postgresql"),
        'NAME': os.getenv('DB_NAME', default="postgres"),
        'USER': os.getenv('POSTGRES_USER', default="postgres"),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default="postgres"),
        'HOST': os.getenv('DB_HOST', default="db"),
        'PORT': os.getenv('DB_PORT', default="5432")
    }
}

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

LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)
TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'core/locale'),
]
STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core/static/'),
    os.path.join(BASE_DIR, 'api/docs/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles/')
MEDIA_URL = '/mediafiles/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.PageNumberLimitPagination',
    'PAGE_SIZE': 6,
}
DJOSER = {
    'SERIALIZERS': {
        'user': 'api.users.serializers.UserSerializer',
        'current_user': 'api.users.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ('djoser.permissions.CurrentUserOrAdminOrReadOnly',),
    },
}
