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
    DEBUG = True
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
elif HOSTNAME == 'serdar-laptop':
    PROJECT_ROOT = '/home/serdar/hadimac/'
    DATABASE_ENGINE = 'sqlite'
    DATABASE_ENGINE = "sqlite3"
    DATABASE_NAME = os.path.join(PROJECT_ROOT,"hadimac.db")
    DEBUG = True
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
elif HOSTNAME == 'butun-desktop':
    PROJECT_ROOT = '/home/butun/hadimac/'
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'hadimac'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'test3142'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '5432'
    DEBUG = True
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'yasso03@gmail.com'
    EMAIL_HOST_PASSWORD = '5166963'
    EMAIL_PORT = 587
    EMAIL_TO ="yasin.meydan@akinon.com"
    ADMINS = (
        ('Yasin Meydan', 'yasin.meydan@akinon.com'),
        )
elif HOSTNAME == "naruto-laptop":
    PROJECT_ROOT="/home/naruto/akinon/hadimac/"
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'hadimac'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = '123456'
    DATABASE_HOST = 'localhost'
    DEBUG = True


MIN_TIME_TO_CANCELATION = datetime.timedelta(days = 2, hours = 0)
LENGTH_OF_FAULT = datetime.timedelta(days = 27, hours = 23, minutes = 59, seconds = 59)

TIME_ZONE = 'Europe/Istanbul'

LANGUAGE_CODE = 'tr-tr'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT,"site_media")

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
