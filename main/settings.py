import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # project root directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media')
STATIC_URL = 'static/'

CACHE_PATH = os.path.join(BASE_DIR, 'cache')

MSE_THRESHOLD = 0.45
SSIM_THRESHOLD = 0.5
VGG16_THRESHOLD = 0.8

UPLOADS_FILES_PATH = 'results/uploads'  # folder for downloadable content

SECRET_KEY = 'django-insecure-4)ycj8^ih^xaq+b3+%0z1zdm&0ufhv29i5mpjdmjum+=_di!l8'

DEBUG = True
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True   # internalization
USE_TZ = True  # time zone support

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'main.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'database.db')
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
