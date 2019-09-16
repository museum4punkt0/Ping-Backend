import os
import sys
from environ import Env

env = Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env('DJANGO_SECRET_KEY', default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'main.apps.MainConfig',
    'storages',
    'django_nose',
    'django.contrib.gis',
    'mapwidgets',
    'nested_admin',
    'admin_tools',
    # 'debug_toolbar'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'main.middleware.debug_middleware.NonHtmlDebugToolbarMiddleware',
]

ROOT_URLCONF = 'mein_objekt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],

        },
    },
]
WSGI_APPLICATION = 'mein_objekt.wsgi.application'

WSGI = 'django.core.wsgi' in sys.modules

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env('POSTGRES_NAME', default=None),
        'USER' : env('POSTGRES_USER', default=None),
        'PASSWORD' : env('POSTGRES_PASSWORD', default=None),
        'HOST' : env('POSTGRES_HOST', default=None),
        'PORT' : env('POSTGRES_PORT', default=5432),
        'TEST': {'NAME': 'mytestdatabase'}
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# local storage
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = ('static/',)

INTERNAL_IPS = ('127.0.0.1',)

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# WSGI = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s:%(name)s: %(message)s '
                      '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'WARNING',
            'formatter': 'main_formatter',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'main_formatter',
            'filename': BASE_DIR + '/server.log',
            'maxBytes': 1024*1024*10, # 10 MB
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'main_formatter',
            'filters': ['require_debug_true'],
        },

    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'logfile'],
            'propagate': False,
        },

    },
}

