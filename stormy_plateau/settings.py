from datetime import timedelta
from os import getenv
from pathlib import Path

import django_heroku
from dotenv import find_dotenv, load_dotenv

# =================================================================================
# SETUP FILES
# =================================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv())
DEBUG = getenv("DEBUG", False)
SECRET_KEY = getenv("SECRET_KEY", "abcdefg12345678")
ALLOWED_HOSTS = (
    "silver-umbrella-2019.herokuapp.com",
    "localhost",
    "127.0.0.1",
)
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
# =================================================================================
# ADMINISTRATIVE
# =================================================================================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = getenv("EMAIL_PORT", 587)
EMAIL_USE_TLS = False
EMAIL_HOST_USER = getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_PASS")
servers = getenv("MEMCACHIER_SERVERS")
username = getenv("MEMCACHIER_USERNAME")
password = getenv("MEMCACHIER_PASSWORD")
# =================================================================================
# APPLICATION
# =================================================================================
# Application definition
THIRD_PARTY_APPS = (
    "djoser",
    # "channels",
    "whitenoise",
    "corsheaders",
    "rest_framework",
)
DEVELOPMENT_APPS = (
    "debug_toolbar",
    "whitenoise.runserver_nostatic",
    "django_extensions",
)
PROJECT_APPS = (
    "users.apps.UsersConfig",
    "blog.apps.BlogConfig",
    "appointments.apps.AppointmentsConfig",
)
DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)
INSTALLED_APPS = THIRD_PARTY_APPS + PROJECT_APPS + DJANGO_APPS

# if "channels" in THIRD_PARTY_APPS:
#     ASGI_APPLICATION = "silver_umbrella.asgi.application"
# else:
WSGI_APPLICATION = "silver_umbrella.wsgi.application"
ROOT_URLCONF = "silver_umbrella.urls"
AUTH_USER_MODEL = "users.User"
# =================================================================================
# CHANNELS / CHAT / WEBSOCKETS
# =================================================================================
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(getenv("REDIS_HOST"), getenv("REDIS_PORT"))],
            # ["unix:///path/to/redis.sock"] # unix domain socket faster than loopback
            #  "symmetric_encryption_keys": [SECRET_KEY],
        },
    },
}
# =================================================================================
# DATABASE / CACHE
# =================================================================================
def get_cache():
    try:
        return {
            "default": {
                "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
                # TIMEOUT is not the connection timeout! It's the default expiration
                # timeout that should be applied to keys! Setting it to `None`
                # disables expiration.
                "TIMEOUT": None,
                "LOCATION": servers,
                "OPTIONS": {
                    "binary": True,
                    "username": username,
                    "password": password,
                    "behaviors": {
                        # Enable faster IO
                        "no_block": True,
                        "tcp_nodelay": True,
                        # Keep connection alive
                        "tcp_keepalive": True,
                        # Timeout settings
                        "connect_timeout": 2000,  # ms
                        "send_timeout": 750 * 1000,  # us
                        "receive_timeout": 750 * 1000,  # us
                        "_poll_timeout": 2000,  # ms
                        # Better failover
                        "ketama": True,
                        "remove_failed": 1,
                        "retry_timeout": 2,
                        "dead_timeout": 30,
                    },
                },
            }
        }
    except:
        return {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}


CACHES = get_cache()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "db_testDB.sqlite3",
        },
    }
}
# =================================================================================
# INTERNATIONALIZATION
# =================================================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
THOUSAND_SEPARATOR = ","
USE_THOUSAND_SEPARATOR = True
NUMBER_GROUPING = 3
# =================================================================================
# REST_FRAMEWORK / API
# =================================================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # "rest_framework.permissions.AllowAny",
        # "rest_framework.permissions.IsAdminUser",
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}
# =================================================================================
# SECURITY
# =================================================================================
validator = "django.contrib.auth.password_validation"
AXES_FAILURE_LIMIT = 3
AXES_ENABLED = False
AXES_COOLOFF_TIME = timedelta(hours=24)
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
# AXES_LOCKOUT_TEMPLATE
# MIDDLEWARE += ("axes.middleware.AxesMiddleware",)
# AUTHENTICATION_BACKENDS = (
#     "axes.backends.AxesBackend",
#     "django.contrib.auth.backends.ModelBackend",
# )
PRODUCTION_MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)
AUTH_PASSWORD_VALIDATORS = (
    {
        "NAME": f"{validator}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{validator}.MinimumLengthValidator",
    },
    {
        "NAME": f"{validator}.CommonPasswordValidator",
    },
    {
        "NAME": f"{validator}.NumericPasswordValidator",
    },
)
# CORS_ORIGIN_WHITELIST = ('localhost')
CORS_ALLOW_ALL_ORIGINS = True
# ACCOUNT_AUTHENTICATION_METHOD = "username"
# ACCOUNT_EMAIL_VERIFICATION = "none"
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
# =================================================================================
# TEMPLATES / STATIC FILES / MEDIA FILES
# =================================================================================
TEMPLATES = (
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
)
SITE_ID = 1
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # [BASE_DIR / "build.static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
LOGIN_REDIRECT_URL = "homepage"
LOGIN_URL = "login"
# =================================================================================
# HEROKU / LINODE / DEPLOYMENT or DEBUG SETTINGS
# =================================================================================
INTERNAL_IPS = ("127.0.0.1",)
if DEBUG:
    INSTALLED_APPS += DEVELOPMENT_APPS
    MIDDLEWARE = (
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ) + PRODUCTION_MIDDLEWARE
else:
    MIDDLEWARE = PRODUCTION_MIDDLEWARE
    django_heroku.settings(locals())
