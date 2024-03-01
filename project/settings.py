
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dbpx)!#%s!#n^&&r^e0!t&ot$vit@t8++_=1*)#84ym)j-v@(w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','192.168.1.5','127.0.0.1','basimyounis.com']


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maindata',
    # 'rangefilter',
    # 'corsheaders',
    # "django_extensions",
    # 'autocomplete_light',
]

X_FRAME_OPTIONS='SAMEORIGIN'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'project.urls'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'http://192.168.1.5',  
    'http://127.0.0.1',  
    'https://basimyounis.com',  
    'https://9e67-41-235-117-105.ngrok-free.app',  
]




TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ar-eg'

TIME_ZONE = 'Africa/Cairo'


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_ROOT = BASE_DIR / "static"
# STATIC_URL = '/static/'
# # STATICFILES_DIRS = [
# #     BASE_DIR / "static",
# #     # '/var/www/static/',
# # ]
# MEDIA_URL = '/media/'
# MEDIA_ROOT=BASE_DIR / "media"



import os
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_TRUSTED_ORIGINS = ['http://192.168.1.5/','http://127.0.0.1/','https://9e67-41-235-117-105.ngrok-free.app']
SECURE_CROSS_ORIGIN_OPENER_POLICY = ['http://192.168.1.5/','http://127.0.0.1/','https://9e67-41-235-117-105.ngrok-free.app']



ADMIN_ORDERING = (
    ('maindata', ('Reserve','Patient','SessionPrice')),
    ('auth', ('User', 'Group')),
    ('admin_interface', ('Theme', )),
    
)


from django.contrib import admin

def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)
    if not app_dict:
        return
    NEW_ADMIN_ORDERING = []
    if app_label:
        for ao in ADMIN_ORDERING:
            if ao[0] == app_label:
                NEW_ADMIN_ORDERING.append(ao)
                break
    if not app_label:
        for app_key in list(app_dict.keys()):
            if not any(app_key in ao_app for ao_app in ADMIN_ORDERING):
                app_dict.pop(app_key)
    app_list = sorted(
        app_dict.values(), key=lambda x: [ao[0] for ao in ADMIN_ORDERING].index(x['app_label'])
    )
    for app, ao in zip(app_list, NEW_ADMIN_ORDERING or ADMIN_ORDERING):
        if app['app_label'] == ao[0]:
            for model in list(app['models']):
                if not model['object_name'] in ao[1]:
                    app['models'].remove(model)
        app['models'].sort(key=lambda x: ao[1].index(x['object_name']))
    return app_list

admin.AdminSite.get_app_list = get_app_list