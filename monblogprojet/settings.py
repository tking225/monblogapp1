import os
from pathlib import Path
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
#     SECRET KEY & DEBUG
# ===========================
SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
     'localhost',
    '127.0.0.1',
    config('RENDER_EXTERNAL_HOSTNAME', default=''),
    'monblogapp1-2.onrender.com',
]

# ===========================
#         INSTALLED APPS
# ===========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Ton app
    'blogapp',
]

# ===========================
#          MIDDLEWARE
# ===========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "monblogprojet.urls"

# ===========================
#           TEMPLATES
# ===========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "monblogprojet.wsgi.application"

# ===========================
#         DATABASE
# ===========================
DATABASE_URL = config("DATABASE_URL", default=None)

if DATABASE_URL:
    # Production : Render utilise PostgreSQL
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Local : fallback vers SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ===========================
#        PASSWORDS
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===========================
#        INTERNATIONAL
# ===========================
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===========================
#         STATIC FILES
# ===========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# ===========================
#         MEDIA FILES
# ===========================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ===========================
#         DEFAULT PRIMARY KEY
# ===========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



LOGIN_REDIRECT_URL = '/' # Redirige vers la page d'accueil (racine) après connexion 
LOGOUT_REDIRECT_URL = '/' # Optionnel : Redirige vers l'accueil après déconnexion (déjà géré par notre vue) 
LOGIN_REDIRECT_URL = '/' # indique à