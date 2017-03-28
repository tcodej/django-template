import os
import requests

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=v02n!vz9pu@!k=c2*hccbas5c$9so22mchs&kgzj-^-l657w4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# add any other relevent host names
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.compute-1.amazonaws.com',  # allows viewing of instances directly
    'example.us-west-2.elasticbeanstalk.com',
]

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get(
        'http://000.000.000.000/latest/meta-data/local-ipv4',
        timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

# Application definition

INSTALLED_APPS = [
    'services.apps.ServicesConfig',
    'redactor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PROJECT_DB_NAME', 'example'),
        'USER': os.environ.get('PROJECT_DB_USER'),
        'PASSWORD': os.environ.get('PROJECT_DB_PASSWORD'),
        'HOST': os.environ.get('PROJECT_DB_HOST', 'localhost'),
        'PORT': 5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_ROOT = os.path.abspath(PROJECT_PATH)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'


# Redactor is a WYSIWYG text editor
REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'

# This environment variable should be set in the Elastic Beanstalk admin panel under Configuration > Software Configuration > Environment Properties
ENVIRONMENT_NAME = os.getenv('ENVIRONMENT_NAME', 'production')
AWS_KEY = os.getenv('AWS_ACCESS_KEY_ID', False)
AWS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY', False)

#todo: change urls below...
CORS_ORIGIN_WHITELIST = (
    'localhost',
    'test.example.com.s3-website-us-west-2.amazonaws.com',
    'www.example.com.s3-website-us-west-2.amazonaws.com',
)  # Add allowed hosts for prodction

# CMS can publish to either test for previewing the front-end or prod
AWS_BUCKET_TEST = 'test.example.com'
AWS_BUCKET_PROD = 'www.example.com'
AWS_BUCKET_REGION = 'us-west-2'

"""
Put any environment specific config here
"""
if ENVIRONMENT_NAME == 'production':
    DEBUG = False    # Set to False for production
    CORS_ORIGIN_ALLOW_ALL = False    # When true, the whitelist is ignored
    LOG_DIR = '/var/log/app'
else:
    CORS_ORIGIN_ALLOW_ALL = True
    LOG_DIR = 'logs'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '%s/django.log' % LOG_DIR,
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'django.request': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

