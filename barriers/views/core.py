from django.conf import settings
from django.views.generic import FormView, TemplateView

from ..forms.search import BarrierSearchForm
from .mixins import BarrierContextMixin

from utils.api_client import MarketAccessAPIClient
from utils.metadata import get_metadata


class Dashboard(TemplateView):
    template_name = "barriers/dashboard.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        sort = self.request.GET.get('sort', '-modified_on')
        watchlists = []
        barriers = []

        client = MarketAccessAPIClient(self.request.session.get('sso_token'))
        user_data = client.get('whoami')
        user_profile = user_data.get('user_profile', None)

        if user_profile:
            watchlists = user_profile.get('watchList', ())
            if watchlists:
                watchlists = watchlists['lists']
                selected_watchlist = int(self.request.GET.get('list', 0))
                watchlists[selected_watchlist]['is_current'] = True

                filters = self.get_watchlist_params(
                    watchlists[selected_watchlist]
                )
                barriers = client.barriers.list(
                    ordering=sort,
                    **filters
                )

        context_data.update({
            'page': 'dashboard',
            'watchlists': watchlists,
            'barriers': barriers,
            'can_add_watchlist': (
                len(watchlists) < settings.MAX_WATCHLIST_LENGTH
            ),
            'sort_field': sort.lstrip('-'),
            'sort_descending': sort.startswith('-'),
        })
        return context_data

    def get_watchlist_params(self, watchlist):
        filter_map = {
            'type': 'barrier_type',
            'search': 'text',
        }
        filters = {
            filter_map.get(name, name): value
            for name, value in watchlist.get('filters').items()
        }

        region = filters.pop('region', [])
        country = filters.pop('country', [])

        if country or region:
            filters['location'] = ",".join(country + region)

        if filters.get('sector'):
            filters['sector'] = ",".join(filters['sector'])

        if 'createdBy' in filters:
            created_by = filters.pop('createdBy')
            if '1' in created_by:
                filters['user'] = 1
            elif '2' in created_by:
                filters['team'] = 1

        return filters


class AddABarrier(TemplateView):
    template_name = "barriers/add_a_barrier.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'page': 'add-a-barrier',
        })
        return context_data


class FindABarrier(FormView):
    template_name = "barriers/find_a_barrier.html"
    form_class = BarrierSearchForm

    def get_context_data(self, form, **kwargs):
        context_data = super().get_context_data(**kwargs)
        client = MarketAccessAPIClient(self.request.session.get('sso_token'))

        barriers = client.barriers.list(
            ordering="-reported_on",
            limit=100,
            offset=0,
            **form.get_search_parameters(),
        )

        context_data.update({
            'barriers': barriers,
            'page': 'find-a-barrier',
        })
        return context_data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['metadata'] = get_metadata()
        kwargs['data'] = self.get_form_data()
        return kwargs

    def get_form_data(self):
        data = dict(self.request.GET)
        if 'search' in data:
            data['search'] = self.request.GET.get('search', "")
        return data

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))


class BarrierDetail(BarrierContextMixin, TemplateView):
    template_name = "barriers/barrier_detail.html"
