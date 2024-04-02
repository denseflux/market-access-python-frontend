"""
Django settings for market_access_python_frontend project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import sys
from pathlib import Path

import dj_database_url
import sentry_sdk
from dbt_copilot_python.database import database_url_from_env
from dbt_copilot_python.utility import is_copilot
from django_log_formatter_asim import ASIMFormatter
from django_log_formatter_ecs import ECSFormatter
from environ import Env
from sentry_sdk.integrations.django import DjangoIntegration

ROOT_DIR = Path(__file__).parents[2]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, ".env")

if os.path.exists(ENV_FILE):
    Env.read_env(ENV_FILE)

env = Env(DEBUG=(bool, False))

# Load PaaS Service env vars
VCAP_SERVICES = env.json("VCAP_SERVICES", default={})

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
# Application definition

ELASTIC_APM_ENABLED = env("ELASTIC_APM_ENABLED", default=not DEBUG)

PRIORITISATION_STRATEGIC_ASSESSMENTS = env.bool(
    "PRIORITISATION_STRATEGIC_ASSESSMENTS", default=False
)

if ELASTIC_APM_ENABLED:
    ELASTIC_APM = {
        "SERVICE_NAME": "market-access-pyfe",
        "SECRET_TOKEN": env("ELASTIC_APM_SECRET_TOKEN"),
        "SERVER_URL": env("ELASTIC_APM_URL"),
        "ENVIRONMENT": env("ENVIRONMENT", default="dev"),
    }

BASE_APPS = [
    # apps that need to load first
    "whitenoise.runserver_nostatic",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.forms",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "webpack_loader",
    "formtools",
    "corsheaders",
]

LOCAL_APPS = [
    "authentication",
    "barriers",
    "core",
    "healthcheck",
    "reports",
    "users",
    "pingdom",
]

INSTALLED_APPS = BASE_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

if ELASTIC_APM_ENABLED:
    INSTALLED_APPS.append("elasticapm.contrib.django")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentication.middleware.SSOMiddleware",
    "utils.middleware.RequestLoggingMiddleware",
    "csp.middleware.CSPMiddleware",
    "utils.middleware.DisableClientCachingMiddleware",
    "utils.middleware.SetPermittedCrossDomainPolicyHeaderMiddleware",
]

ROOT_URLCONF = "config.urls"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(ROOT_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.context_processors.user_scope",
                "utils.context_processors.feature_flags",
                "django_settings_export.settings_export",
            ],
            "builtins": [
                "core.templatetags.govuk_forms",
                "users.templatetags.permissions",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if is_copilot():
    DATABASES = {
        "default": dj_database_url.config(
            default=database_url_from_env("DATABASE_ENV_VAR_KEY")
        )
    }
else:
    DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"
STATICFILES_DIRS = [
    str(ROOT_DIR / "core/frontend/dist/"),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

TRUSTED_USER_TOKEN = "ssobypass"

USER_DATA_CACHE_TIME = 3600
METADATA_CACHE_TIME = "10600"
USE_S3_FOR_CSV_DOWNLOADS = env("USE_S3_FOR_CSV_DOWNLOADS", default=True)

# CACHE / REDIS
# Try to read from PaaS service env vars first
REDIS_DB = env.int("REDIS_DB", default=4)
if "redis" in VCAP_SERVICES:
    REDIS_URI = VCAP_SERVICES["redis"][0]["credentials"]["uri"]
else:
    REDIS_URI = env("REDIS_URI")
REDIS_URI = f"{REDIS_URI}/{REDIS_DB}"

if REDIS_URI:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URI,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

# Market access API
MARKET_ACCESS_API_URI = env("MARKET_ACCESS_API_URI")
MARKET_ACCESS_API_HAWK_ID = env("MARKET_ACCESS_API_HAWK_ID")
MARKET_ACCESS_API_HAWK_KEY = env("MARKET_ACCESS_API_HAWK_KEY")
MARKET_ACCESS_API_HAWK_CREDS = {
    "id": MARKET_ACCESS_API_HAWK_ID,
    "key": MARKET_ACCESS_API_HAWK_KEY,
    "algorithm": "sha256",
}

SSO_CLIENT = env("SSO_CLIENT")
SSO_SECRET = env("SSO_SECRET")
SSO_API_URI = env("SSO_API_URI")
SSO_API_TOKEN = env("SSO_API_TOKEN")
SSO_AUTHORIZE_URI = env("SSO_AUTHORIZE_URI")
SSO_BASE_URI = env("SSO_BASE_URI")
SSO_TOKEN_URI = env("SSO_TOKEN_URI")
SSO_MOCK_CODE = env("SSO_MOCK_CODE", default=None)
OAUTH_PARAM_LENGTH = env("OAUTH_PARAM_LENGTH", default=75)

DATAHUB_DOMAIN = env("DATAHUB_DOMAIN", default="https://www.datahub.trade.gov.uk")
DATAHUB_URL = env("DATAHUB_URL")
DATAHUB_HAWK_ID = env("DATAHUB_HAWK_ID")
DATAHUB_HAWK_KEY = env("DATAHUB_HAWK_KEY")

FILE_MAX_SIZE = env.int("FILE_MAX_SIZE", default=(5 * 1024 * 1024))
FILE_SCAN_MAX_WAIT_TIME = env.int("FILE_SCAN_MAX_WAIT_TIME", default=30000)
FILE_SCAN_STATUS_CHECK_INTERVAL = env.int(
    "FILE_SCAN_STATUS_CHECK_INTERVAL", default=500
)
ALLOWED_FILE_TYPES = env.list("ALLOWED_FILE_TYPES", default=["text/csv", "image/jpeg"])

API_RESULTS_LIMIT = env.int("API_RESULTS_LIMIT", default=50)

API_BARRIER_LIST_DEFAULT_SORT = env.str(
    "API_BARRIER_LIST_DEFAULT_SORT", default="-reported_on"
)

# Logging
# ============================================
DJANGO_LOG_LEVEL = env("DJANGO_LOG_LEVEL", default="info").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "asim_formatter": {"()": ASIMFormatter},
        "ecs_formatter": {"()": ECSFormatter},
        "simple": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "asim": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # noqa F405
            "formatter": "asim_formatter",
        },
        "ecs": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # noqa F405
            "formatter": "ecs_formatter",
        },
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,  # noqa F405
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["asim", "ecs", "stdout"],
        "level": os.getenv("ROOT_LOG_LEVEL", "INFO"),  # noqa F405
    },
    "loggers": {
        "django": {
            "handlers": ["asim", "ecs", "stdout"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),  # noqa F405
            "propagate": False,
        },
        "django.server": {
            "handlers": ["asim", "ecs", "stdout"],
            "level": os.getenv("DJANGO_SERVER_LOG_LEVEL", "ERROR"),  # noqa F405
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["asim", "ecs", "stdout"],
            "level": os.getenv("DJANGO_DB_LOG_LEVEL", "ERROR"),  # noqa F405
            "propagate": False,
        },
    },
}


# Django Log Formatter ASIM settings
if is_copilot():
    DLFA_TRACE_HEADERS = ("X-B3-TraceId", "X-B3-SpanId")


DLFE_APP_NAME = True
DLFE_LOG_SENSITIVE_USER_DATA = True

# Google Tag Manager
GTM_ID = env("GTM_ID", default=None)
GTM_AUTH = env("GTM_AUTH", default=None)
GTM_PREVIEW = env("GTM_PREVIEW", default=None)

if not DEBUG:
    sentry_sdk.init(
        dsn=env("SENTRY_DSN"),
        environment=env("SENTRY_ENVIRONMENT"),
        integrations=[
            DjangoIntegration(),
        ],
    )

# Settings made available in templates
SETTINGS_EXPORT = (
    "DJANGO_ENV",
    "DATAHUB_DOMAIN",
    "GTM_ID",
    "GTM_AUTH",
    "GTM_PREVIEW",
)

ACTION_PLANS_ENABLED = env.bool("ACTION_PLANS_ENABLED", default=False)
NEW_ACTION_PLANS_ENABLED = env.bool("NEW_ACTION_PLANS_ENABLED", default=False)

# Webpack config

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "webpack_bundles/",  # must end with slash
        "STATS_FILE": os.path.join(ROOT_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    },
    "REACT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "webpack_bundles/",  # must end with slash
        "STATS_FILE": os.path.join(ROOT_DIR, "webpack-stats-react.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    },
}

# External URLs used within the app
EXTERNAL_URLS_FIND_EXPORTERS = env.str("EXTERNAL_URLS_FIND_EXPORTERS", "")

# Company house config
COMPANIES_HOUSE_API_KEY = env("COMPANIES_HOUSE_API_KEY")
COMPANIES_HOUSE_API_ENDPOINT = env("COMPANIES_HOUSE_API_ENDPOINT")

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = (
    "'self'",
    "https://www.googletagmanager.com/",
    "https://*.google-analytics.com",
    "https://www.google-analytics.com",
)
CSP_CONNECT_SRC = CSP_SCRIPT_SRC
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_REPORT_URI = "/csp_report"
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_REPORT_ONLY = True

# Override to allow admin permission group to be managed. (For local and dev envs)
DISPLAY_ROLE_ADMIN_GROUP = False
