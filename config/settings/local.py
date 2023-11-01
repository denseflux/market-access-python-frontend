from django.utils.log import DEFAULT_LOGGING

from .base import *  # noqa

DJANGO_ENV = "local"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
DEBUG = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            # exact format is not important, this is the minimum information
            "format": "[%(asctime)s] %(name)s %(levelname)5s - %(message)s",
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        # root logger
        "": {
            "level": "WARNING",
            "handlers": ["console"],
        },
        "market-access-python-frontend": {
            "level": DJANGO_LOG_LEVEL,  # noqa
            "handlers": ["console"],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
    },
}

# The following are extra-permission groups (not roles)
# Adding a user to these groups should not remove the role from the user
# Local environments have an extra user permission group to allow
# editing of user profiles without admin access
USER_ADDITIONAL_PERMISSION_GROUPS = [
    "Download approved user",
    "Action plan user",
    "PB100 barrier approver",
    "Role administrator",
]
