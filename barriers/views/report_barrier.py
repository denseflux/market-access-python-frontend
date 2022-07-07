from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from barriers.constants import Statuses
from barriers.models.barriers import Barrier
from barriers.views.mixins import BarrierMixin
from reports.models import Report
from reports.report_views import ReportViewBase
from reports.views import ReportsTemplateView
from utils.api.client import MarketAccessAPIClient
from utils.exceptions import APIHttpException


def get_hs_commodity_answers(barrier: Report):
    """
     Ok so for this part a new view was brought in scope
     so we need to address this independently and will have to
     be treated differently in the template

    Example output:
    {
        "UK": {
            "name": "UK commodity codes",
            "value": [{
                "code": "120345",
                "name": "Aluminium"
            }]
        },
        "EU": {
            "name": "EU commodity codes",
            "value": [{
                "code": "120345",
                "name": "Aluminium"
            }]
        }
    }

    Reason we return a list of object is so the template can format them into a table
    """
    hs_commodity_answers = {}
    for commodity in barrier.commodities:
        # if the commodity is not in the hs_commodity_answers dict, add it
        commodity_country = commodity["country"]["name"]
        if commodity_country not in hs_commodity_answers:
            hs_commodity_answers[commodity_country] = {
                "name": f"{commodity_country} commodity codes",
                "value": [],
            }
        # add the commodity to the list of commodities for the country
        hs_commodity_answers[commodity_country]["value"].append(
            {
                "code": commodity["code"],
                "name": commodity["commodity"]["full_description"],
            }
        )
    return hs_commodity_answers.values()


def get_report_barrier_answers(barrier: Report):

    check_answers_page_url = reverse(
        "reports:report_barrier_answers", kwargs={"barrier_id": barrier.id}
    )
    # query_string with next = check_answers_page_url
    qs = "?next={}".format(check_answers_page_url)

    hs_commodity_questions = {}
    for commodity in barrier.commodities:
        country = commodity["country"]["name"]
        if country not in hs_commodity_questions.keys():
            hs_commodity_questions[country] = {
                "name": f"{country} commodity codes",
                "value": "",
            }
        hs_commodity_questions[country][
            "value"
        ] += f"{commodity['commodity']['full_description']},\n"

    return [
        {
            "name": "About the barrier",
            "url": reverse(
                "reports:barrier_about_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": [
                {
                    "name": "Name of the barrier",
                    "value": barrier.title,
                },
                {
                    "name": "Describe the barrier",
                    "value": barrier.summary,
                },
                {
                    "name": "Does the summary contain OFFICIAL-SENSITIVE information?",
                    "value": barrier.is_summary_sensitive,
                },
                {
                    "name": "What product, service or investment is affected?",
                    "value": barrier.product,
                },
                {
                    "name": "Who told you about the barrier?",
                    "value": barrier.source_display,  # barrier.reported_by,
                },
                {
                    "name": (
                        "Is this issue caused by or related to any of the following?"
                    ),
                    "value": ",\n".join([tag["title"] for tag in barrier.tags]),
                },
            ],
        },
        {
            "name": "Barrier status",
            "url": reverse(
                "reports:barrier_status_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": [
                {
                    "name": "What type of barrier is it?",
                    "value": barrier.term.get("name"),  # barrier.barrier_type,
                },
                {
                    "name": "What is the status of the barrier?",
                    "value": barrier.status_display,
                },
                {
                    "name": "Who is due to take action?",
                    "value": barrier.sub_status_display or "-",
                },
                {
                    "name": "Describe briefly why this barrier is pending action",
                    "value": barrier.status_summary
                    if barrier.is_status(Statuses.OPEN_PENDING_ACTION)
                    else "-",
                },
                {
                    "name": "Describe briefly why work on this barrier is in progress",
                    "value": barrier.status_summary
                    if barrier.is_status(Statuses.OPEN_IN_PROGRESS)
                    else "-",
                },
                {
                    "name": "Date the barrier was partially resolved",
                    "value": barrier.status_date
                    if barrier.is_status(Statuses.RESOLVED_IN_PART)
                    else "-",
                },
                {
                    "name": "Describe briefly how this barrier was partially resolved",
                    "value": barrier.status_summary
                    if barrier.is_status(Statuses.RESOLVED_IN_PART)
                    else "-",
                },
                {
                    "name": "Date the barrier was resolved",
                    "value": barrier.status_date
                    if barrier.is_status(Statuses.RESOLVED_IN_FULL)
                    else "-",
                },
                {
                    "name": "Describe briefly how this barrier was fully resolved",
                    "value": barrier.status_summary
                    if barrier.is_status(Statuses.RESOLVED_IN_FULL)
                    else "-",
                },
                {
                    "name": "Describe briefly why this barrier is dormant",
                    "value": barrier.status_summary
                    if barrier.is_status(Statuses.DORMANT)
                    else "-",
                },
            ],
        },
        {
            "name": "Location of the barrier",
            "url": reverse(
                "reports:barrier_location_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": [
                {
                    "name": "Which location is affected by this issue?",
                    "value": barrier.location,
                },
                {
                    "name": (
                        "Was this barrier caused by a regulation introduced by the"
                        " EAEU?"
                    ),
                    "value": barrier.data.get("caused_by_trading_bloc", "-") or "-",
                },
                {
                    "name": "Does it affect the entire country?",
                    "value": barrier.data.get("caused_by_admin_areas", "-"),
                },
                {
                    "name": "Which trade direction does this barrier affect?",
                    "value": barrier.trade_direction_display,
                },
            ],
        },
        {
            "name": "Sectors affected by the barrier",
            "url": reverse(
                "reports:barrier_has_sectors_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": [
                {
                    "name": (
                        "Do you know the sector or sectors affected by the barrier?"
                    ),
                    "value": barrier.sectors_affected,
                },
                {
                    "name": (
                        "Do you know the sector or sectors affected by the barrier?"
                    ),
                    "value": ",\n".join(
                        [sector.get("name") for sector in barrier.sectors]
                    )
                    or "-",
                },
            ],
        },
        {
            "name": "Barrier category",
            "url": reverse(
                "reports:barrier_categories_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": [
                {
                    "name": "Define barrier category",
                    "value": ",\n".join(
                        [category.get("title") for category in barrier.categories]
                    ),
                }
            ],
        },
        {
            "name": "Add HS commodity codes",
            "type": "hs_commodity_codes",
            "url": reverse(
                "reports:barrier_commodities_uuid", kwargs={"barrier_id": barrier.id}
            )
            + qs,
            "questions": get_hs_commodity_answers(barrier),
        },
    ]


class ReportBarrierAnswersView(ReportViewBase):
    template_name = "barriers/report_barrier_answers.html"
    _client: MarketAccessAPIClient = None

    def post(self, request, *args, **kwargs):
        if self.barrier.draft:
            self.client.reports.submit(self.barrier.id)
        return HttpResponseRedirect(
            reverse("barriers:barrier_detail", kwargs={"barrier_id": self.barrier.id})
        )

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        barrier_id = kwargs.get("barrier_id")
        barrier = self.get_draft_barrier(barrier_id)
        context_data["barrier"] = barrier
        context_data["report_barrier_answers"] = get_report_barrier_answers(barrier)
        return context_data
