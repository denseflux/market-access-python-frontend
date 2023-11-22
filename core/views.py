import logging

import sentry_sdk
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from authentication.decorators import public_view

logger = logging.getLogger(__name__)


@public_view
@method_decorator(csrf_exempt, name="dispatch")
class CSPReportView(View):
    def post(self, request, *args, **kwargs):
        with sentry_sdk.configure_scope() as scope:
            report = request.body.decode("utf-8")
            scope.set_tag("type", "csp_report")
            logger.error("CSP Blocked", extra={"report": report})
        return HttpResponse(status=200)
