"""
Django settings for multyproject project.
"""

from pathlib import Path
import os
import dj_database_url # ✅ IMPORTANTE: Para manejar la URL de la BD de Render


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!3ke$yj@d*^ur88^p3c#8gz@bca_xz7dariqp11n=c%bq-a(ff'

# =========================================================
# 1. CONFIGURACIÓN DE SEGURIDAD Y ENTORNO (CRÍTICO)
# =========================================================

# ✅ DEBUG: Se desactiva en producción si la variable RENDER_EXTERNAL_HOSTNAME existe.
# Usaremos False por defecto, ya que es lo que has indicado.
DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    # ✅ Añadir el dominio de Render y Streamlit Cloud para seguridad extra
    os.environ.get("RENDER_EXTERNAL_HOSTNAME"),
    "*.onrender.com",
    "*.streamlit.app",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'import_export',
    "corsheaders",
    'apilogistica',
    'procesamiento',
    'users',
    'rest_framework',
    'djoser',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ✅ WHITENOISE debe ir después de SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ✅ CORS debe ir lo más alto posible, antes de CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'multyproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'multyproject.wsgi.application'


# =========================================================
# 2. CONFIGURACIÓN DE BASE DE DATOS (CRÍTICO PARA RENDER)
# =========================================================
if os.environ.get('DATABASE_URL'):
    # ✅ PRODUCCIÓN: Usa la URL de la BD inyectada por Render (PostgreSQL o MySQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    # ✅ DESARROLLO: Usa SQLite si no hay DATABASE_URL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # ... (tus validadores permanecen iguales) ...
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =========================================================
# 3. ARCHIVOS ESTÁTICOS (WHITENOISE)
# =========================================================
STATIC_URL = "/static/"
# ✅ Ruta de colección de estáticos
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles") 
# ✅ Almacenamiento con Whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    # ... (Tu configuración de DRF) ...
}

DJOSER = {
    # ... (Tu configuración de Djoser) ...
}

SPECTACULAR_SETTINGS = {
    # ... (Tu configuración de Spectacular) ...
}


# =========================================================
# 4. CONFIGURACIÓN DE SEGURIDAD ADICIONAL (CORS/CSRF)
# =========================================================

# ✅ Requerido para Render (manejo de SSL)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ✅ CORS: Permitir todas las peticiones (ya que es una API pública)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF: Permitir peticiones POST desde Streamlit y Render
# Esto es CRÍTICO para que el registro (POST) funcione desde tu frontend.
CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "http://localhost:8501", 
    "https://*.streamlit.app", 
]