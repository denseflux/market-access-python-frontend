from .test import *  # noqa

DJANGO_ENV = "front_end_tests"

HEADLESS = env.bool("HEADLESS", default=True)

BASE_FRONTEND_TESTING_URL = env.str(
    "BASE_FRONTEND_TESTING_URL", default="http://web:9000"
)
if BASE_FRONTEND_TESTING_URL.endswith("/"):
    BASE_FRONTEND_TESTING_URL = BASE_FRONTEND_TESTING_URL[:-1]
