from http import HTTPStatus

from django.urls import resolve, reverse
from mock import patch

from barriers.views.public_barriers import PublicBarrierDetail
from core.tests import MarketAccessTestCase


class PublicBarrierViewTestCase(MarketAccessTestCase):
    def test_public_barrier_url_resolves_to_correct_view(self):
        match = resolve(f'/barriers/{self.barrier["id"]}/public/')
        assert match.func.view_class == PublicBarrierDetail

    @patch("utils.api.client.PublicBarriersResource.get")
    @patch("utils.api.client.PublicBarriersResource.get_activity")
    @patch("utils.api.client.PublicBarriersResource.get_notes")
    def test_public_barrier_view_loads_correct_template(
        self, _mock_get_notes, _mock_get_activity, mock_get
    ):
        mock_get.return_value = self.barrier
        url = reverse(
            "barriers:public_barrier_detail", kwargs={"barrier_id": self.barrier["id"]}
        )

        response = self.client.get(url)

        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, "barriers/public_barriers/detail.html")

    @patch("utils.api.client.PublicBarriersResource.get")
    @patch("utils.api.client.PublicBarriersResource.get_activity")
    @patch("utils.api.client.PublicBarriersResource.get_notes")
    def test_public_barrier_view_loads_html(
        self, _mock_get_notes, _mock_get_activity, mock_get
    ):
        mock_get.return_value = self.public_barrier
        url = reverse(
            "barriers:public_barrier_detail", kwargs={"barrier_id": self.barrier["id"]}
        )
        title = "<title>Market Access - Public barrier</title>"
        section_head = '<h2 class="summary-group__heading">Public view:'
        notes_head = '<h2 class="section-heading govuk-!-margin-bottom-0">Internal notes and updates</h2>'
        add_note_button = (
            '<a class="govuk-button button--primary" href="?add-note=1">Add a note</a>'
        )

        response = self.client.get(url)
        html = response.content.decode("utf8")

        assert HTTPStatus.OK == response.status_code
        assert title in html
        assert section_head in html
        assert notes_head in html
        assert add_note_button in html

    @patch("utils.api.resources.APIResource.list")
    @patch("utils.api.client.PublicBarriersResource.get")
    @patch("utils.api.client.PublicBarriersResource.get_activity")
    @patch("utils.api.client.PublicBarriersResource.get_notes")
    def test_public_barrier_search_view_loads_html(
        self, _mock_get_notes, _mock_get_activity, mock_get, mock_list
    ):
        mock_get.return_value = self.public_barrier
        url = reverse("barriers:public_barriers")
        title = "<title>Market Access - Public barriers</title>"
        section_head = '<h1 class="govuk-heading-l govuk-!-margin-bottom-5">Market access public barriers</h1>'

        response = self.client.get(url)
        html = response.content.decode("utf8")

        assert HTTPStatus.OK == response.status_code
        assert title in html
        assert section_head in html

    @patch("utils.api.resources.APIResource.list")
    @patch("utils.api.client.PublicBarriersResource.get")
    @patch("utils.api.client.PublicBarriersResource.get_activity")
    @patch("utils.api.client.PublicBarriersResource.get_notes")
    def test_public_barrier_search_view_filters_correctly(
        self, _mock_get_notes, _mock_get_activity, mock_get, mock_list
    ):
        def fetch_html_for_params(params):
            url = reverse("barriers:public_barriers")
            response = self.client.get(url, data=params)
            html = response.content.decode("utf8")
            return html, response

        html, response = fetch_html_for_params(
            {
                "country": [
                    "9f5f66a0-5d95-e211-a939-e4115bead28a",
                    "83756b9a-5d95-e211-a939-e4115bead28a",
                ],
                "sector": [
                    "9538cecc-5f95-e211-a939-e4115bead28a",
                    "aa22c9d2-5f95-e211-a939-e4115bead28a",
                ],
                "region": [
                    "3e6809d6-89f6-4590-8458-1d0dab73ad1a",
                    "5616ccf5-ab4a-4c2c-9624-13c69be3c46b",
                ],
                "status": ["0", "10", "30"],
            }
        )

        form = response.context["form"]
        assert HTTPStatus.OK == response.status_code

        assert form.cleaned_data["country"] == [
            "9f5f66a0-5d95-e211-a939-e4115bead28a",
            "83756b9a-5d95-e211-a939-e4115bead28a",
        ]

        assert form.cleaned_data["sector"] == [
            "9538cecc-5f95-e211-a939-e4115bead28a",
            "aa22c9d2-5f95-e211-a939-e4115bead28a",
        ]

        assert form.cleaned_data["region"] == [
            "3e6809d6-89f6-4590-8458-1d0dab73ad1a",
            "5616ccf5-ab4a-4c2c-9624-13c69be3c46b",
        ]

        assert form.cleaned_data["status"] == ["0", "10", "30"]

        mock_list.assert_called_with(
            country=",".join(
                [
                    "9f5f66a0-5d95-e211-a939-e4115bead28a",
                    "83756b9a-5d95-e211-a939-e4115bead28a",
                ]
            ),
            sector=",".join(
                [
                    "9538cecc-5f95-e211-a939-e4115bead28a",
                    "aa22c9d2-5f95-e211-a939-e4115bead28a",
                ]
            ),
            region=",".join(
                [
                    "3e6809d6-89f6-4590-8458-1d0dab73ad1a",
                    "5616ccf5-ab4a-4c2c-9624-13c69be3c46b",
                ]
            ),
            status=",".join(["0", "10", "30"]),
        )
