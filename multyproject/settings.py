import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# CRÍTICO: Cargar variables de .env/.env_temp inmediatamente
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# CONFIGURACIONES CRÍTICAS DE SEGURIDAD Y ENTORNO
# ----------------------------------------------------

# 1. SECRET_KEY: Leída de Render o del archivo .env_temp
# Render: Lo lee de la variable de entorno que definiste.
SECRET_KEY = os.environ.get('SECRET_KEY')

# 2. DEBUG: Debe ser False en producción (Render)
# En Render, se recomienda usar 'False'. Para local, puedes usar 'True' en .env.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 3. ALLOWED_HOSTS: Determinado por el host de Render para evitar el error 500
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if RENDER_EXTERNAL_HOSTNAME:
    # Acepta la URL pública de Render y su subdominio (www.)
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, f'www.{RENDER_EXTERNAL_HOSTNAME}']
else:
    # Hosts permitidos para desarrollo local
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 4. Configuración de Base de Datos (PostgreSQL vs. SQLite)
# Intenta usar DATABASE_URL de Render, si no existe (localmente), usa SQLite.
if os.environ.get('DATABASE_URL'):
    # PostgreSQL (Producción en Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
    print("Conexión: Usando PostgreSQL de Render.")
else:
    # SQLite (Desarrollo Local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("Conexión: Usando base de datos local (SQLite).")

# ----------------------------------------------------
# APPLICATION DEFINITION
# ----------------------------------------------------

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
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # IMPORTANTE para archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ... (El resto de configuraciones como ROOT_URLCONF, TEMPLATES, etc. se mantienen igual)
WSGI_APPLICATION = 'multyproject.wsgi.application'

# ----------------------------------------------------
# STATIC FILES Y WHITENOISE
# ----------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ... (El resto de configuraciones como AUTH_PASSWORD_VALIDATORS, DJOSER, SPECTACULAR_SETTINGS)

# --- Password validation ---
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


# --- Internationalization ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.CustomUser'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


DJOSER = {
    'TOKEN_MODEL': None, 
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer', 
        'user': 'users.serializers.CustomUserSerializer', 
    }
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'API Logística de Multi-Project', 
    'DESCRIPTION': 'Documentación de la API para la gestión de logística.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True