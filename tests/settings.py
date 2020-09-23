import os

DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WSGI_APPLICATION = 'wsgi.application'

OBJECT_CHECKERS_MODULE = 'tests.checkers'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'object_checker',
    'tests',
)

DATABASE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
    },
}

MIDDLEWARE = []

USE_TZ = True
TIME_ZONE = 'UTC'
SECRET_KEY = 'g>Q3Y>VDJ7s};)-g>2Csjz&7FYRm"F?A@QX#"<AXlJfC>a!v&GTL[ey]nE`?cJL'
