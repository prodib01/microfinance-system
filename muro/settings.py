from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = 'django-insecure-d&t7ktt2gf*ec!yhuwr_hl_+f3xr3s%89ht&78+iw6jmbq2p)#'

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "*",
]


INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

INSTALLED_APPS = [
    'jazzmin',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    # 'django_browser_reload',
    'users',
    'branch',
    'loan',
    'clientApp',
    'homeApp',
    'accounting',
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
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'muro.urls'

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
        'libraries':{
            'custom_filters': 'loan.custom_filters',
            
            }
        },
    },
]

WSGI_APPLICATION = 'muro.wsgi.application'

DATABASES = {"default": dj_database_url.config(
    default=os.getenv("DATABASE_URL"))}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


STATICFILES_DIRS = [
    BASE_DIR / "theme/static",
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TAILWIND_APP_NAME = 'theme'

AUTH_USER_MODEL = 'users.MuroUser'

AUTHENTICATION_BACKENDS = [
    "users.backends.MuroUserAuthBackend",
]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kunoomaking@gmail.com'
EMAIL_HOST_PASSWORD = 'sfhy ytrs mbwu dxdb'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# https://muro.nalongonjalasupermarket.com/
CSRF_TRUSTED_ORIGINS = [
    'https://muro.nalongonjalasupermarket.com', 
    'http://localhost/', 
    'http://127.0.0.1/',
    'https://*.nalongonjalasupermarket.com',
    'https://web-production-12a9c.up.railway.app',
    ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
X_FRAME_OPTIONS = 'SAMEORIGIN'