import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY SETTINGS
# ==========================================
# Pull sensitive data from environment variables. Fallback is for local dev only.
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY', 
    'django-insecure-1#i1$%ra=$obdp3b%&5y4$)w-yy*2$*+&2r-l1@2ns(rqkzjft'
)

# NEVER set DEBUG to True in production!
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Allow hosts via environment variable (e.g., "localhost,127.0.0.1,mydomain.com")
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# ==========================================
# APPLICATION DEFINITION
# ==========================================
INSTALLED_APPS = [
    # Default Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',
    'drf_yasg',
    # Note: If you are building a frontend that runs on a different port, 
    # you will likely need 'corsheaders' installed here.

    # Your Apps
    'milestone1.enrollment_aadhaar',
    'milestone1.abha_profile',
    'milestone1.enrollment_mobile',
    'milestone1.enrollment_dl',
    'milestone1.enrollment_biometric',
    'milestone1.abha_login',
    'milestone1.mobile_login',
    'milestone1.abha_search',
    'milestone1.profile_update',
    'milestone1.abhanumber_recover',

    # ✅ Add Milestone 2 App Here
    'milestone2.gateway_auth',
    'milestone2.bridge_update',
    'milestone2.facility_linkage',
    'milestone2.bridge_search',
    'milestone2.gateway_config',
    'milestone2.link_token',
    'milestone2.care_context',
    'milestone2.notify_update',
    'milestone2.sms_notify',
    'milestone2.hiu_discover',
    'milestone2.hiu_on_init',
    'milestone2.hiu_on_confirm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Recommended for static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',      # Uncomment if using django-cors-headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Abdm_Integration.urls'

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # ✅ Your new templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',        # ✅ Fixes admin.W411
                'django.contrib.auth.context_processors.auth',       # ✅ Fixes admin.E402
                'django.contrib.messages.context_processors.messages', # ✅ Fixes admin.E404
            ],
        },
    },
]

WSGI_APPLICATION = 'Abdm_Integration.wsgi.application'


# ==========================================
# DATABASE
# ==========================================
# For production, it's highly recommended to use PostgreSQL via dj-database-url
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================================
# PASSWORD VALIDATION
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==========================================
# DJANGO REST FRAMEWORK & SWAGGER
# ==========================================
REST_FRAMEWORK = {
    # Good practice to define default authentication and permission classes
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # Add Token/JWT authentication here if your API uses it
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Change to IsAuthenticated for production
    ],
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter: Bearer <your_token>'
        }
    }
}


# ==========================================
# INTERNATIONALIZATION
# ==========================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==========================================
# STATIC FILES (CSS, JavaScript, Images)
# ==========================================
STATIC_URL = 'static/'

# Required for production deployment (where 'collectstatic' dumps files)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Extra directories where static files may be stored
STATICFILES_DIRS = []


# ==========================================
# DEFAULT AUTO FIELD
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'django_local_cache',
    }
}