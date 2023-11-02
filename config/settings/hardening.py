from environ import Env

env = Env()

SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 3600

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://www.googletagmanager.com/", "'unsafe-inline'")

CSP_REPORT_URI = env.str("CSP_REPORT_URI", default=None)
CSP_REPORT_ONLY = env.bool("CSP_REPORT_ONLY", default=True)

CORS_ALLOWED_ORIGINS = env.list("ALLOWED_HOSTS", default=[])
