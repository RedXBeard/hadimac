# Django settings for hadimac project.

import os, datetime
from socket import gethostname

HOSTNAME = gethostname()
HOSTS = ['tame']
PRODUCTION = HOSTNAME in HOSTS

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('Ahmet Akin KOK', 'akin.kok@akinon.com'),
    ('Oguz Aylanc', 'oguz.aylanc@akinon.com')
)

MANAGERS = ADMINS

SERVER_EMAIL = "error@hadimac.com"

if PRODUCTION:
    PROJECT_ROOT = '/srv/hadimac/'
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'hadimac'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '12345'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
elif HOSTNAME == 'monster':
    PROJECT_ROOT = '/home/aakok/akinon/hadimac/'
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'hadimac'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '12345'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DEBUG = True
    ADMINS = (
        ('Ahmet Akin KOK', 'akin.kok@akinon.com'),
        )
elif HOSTNAME == 'ege-laptop':
    PROJECT_ROOT = '/home/ege/hadimac/'
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'hadimac'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '1313'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DEBUG = True
    ADMINS = (
        ('Ege Hanoglu', 'ege.hanoglu@akinon.com'),
        )

MIN_TIME_TO_CANCELATION = datetime.timedelta(days = 2, hours = 12)


TIME_ZONE = 'Europe/Istanbul'

LANGUAGE_CODE = 'tr-tr'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = ''

MEDIA_URL = ''

ADMIN_MEDIA_PREFIX = '/media/'

SECRET_KEY = 'egnbp=tsieegf@u35)wfn7#+n!k2t=8v#zr7njy#!p$xbp*9#s'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'hadimac.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'hadimac.user',
    'hadimac.mac',
    'hadimac.comment',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.core.context_processors.media",
    "django.core.context_processors.request",
)


AUTHENTICATION_BACKENDS = (
    "hadimac.authenticators.Authenticate",
)

LOGIN_URL = '/'
LOGOUT_URL = 'logout/'
