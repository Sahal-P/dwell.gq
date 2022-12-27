
import os
from pathlib import Path
import environ

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'category',
    'pages',
    'cart',
    'orders',
    'wishlist',
    'user_profile',
    'offer',
    'coupen',
    'variation',
    'wallet',
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

SECURE_CROSS_ORIGIN_OPENER_POLICY ='unsafe-none'


ROOT_URLCONF = 'dwell.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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


WSGI_APPLICATION = 'dwell.wsgi.application'

AUTH_USER_MODEL ='accounts.Account'




DATABASES = {
'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       
       'NAME': 'dwell',
       
       'USER': 'postgres',
       
       'PASSWORD': env('DATA_BASE_PASSWORD'),

       'HOST': 'localhost',

       'PORT': '5432',

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL ='static/'


STATICFILES_DIRS =[os.path.join(BASE_DIR, 'static'),]

MEDIA_URL ='/media/'

MEDIA_ROOT =BASE_DIR/'media'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SID_TWILIO = env('SID_TWILIO')

TOKEN_TWILIO = env('TOKEN_TWILIO')

RAZOR_ID = env('RAZOR_ID')

RAZOR_SECRET = env('RAZOR_SECRET')

TWILIO_PHONE = env('TWILIO_PHONE')
