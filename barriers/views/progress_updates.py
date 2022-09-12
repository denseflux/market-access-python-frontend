# add and edit views for progress updates
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from barriers.forms.edit import (
    ProgrammeFundProgressUpdateForm,
    Top100ProgressUpdateForm,
)
from barriers.forms.various import ChooseUpdateTypeForm
from barriers.views.mixins import APIBarrierFormViewMixin, BarrierMixin


class ChooseProgressUpdateTypeView(BarrierMixin, FormView):
    template_name = "barriers/progress_updates/choose_type.html"
    form_class = ChooseUpdateTypeForm
    success_url_patterns = {
        "top_100_priority": "barriers:add_top_100_progress_update",
        "programme_fund": "barriers:add_programme_fund_progress_update",
    }

    def get_context_data(self, **kwargs):
        kwargs["barrier_id"] = self.kwargs["barrier_id"]
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        success_url_pattern = self.success_url_patterns.get(
            form.cleaned_data["update_type"]
        )
        self.success_url = reverse(
            success_url_pattern, kwargs={"barrier_id": self.kwargs["barrier_id"]}
        )
        return super().form_valid(form)


class BarrierAddTop100ProgressUpdate(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/progress_updates/add_top_100_update.html"
    form_class = Top100ProgressUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        return kwargs


class BarrierAddProgrammeFundProgressUpdate(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/progress_updates/add_programme_fund_update.html"
    form_class = ProgrammeFundProgressUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        return kwargs


class BarrierEditProgressUpdate(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/progress_updates/edit_top_100.html"
    form_class = Top100ProgressUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = str(self.kwargs.get("barrier_id"))
        kwargs["progress_update_id"] = str(self.kwargs.get("progress_update_id"))
        return kwargs

    def get_initial(self):
        progress_update = next(
            (
                item
                for item in self.barrier.progress_updates
                if item["id"] == str(self.kwargs.get("progress_update_id"))
            ),
            None,
        )
        updates = self.barrier.progress_updates
        progress_update_id = self.kwargs.get("progress_update_id")
        return {
            "status": progress_update["status"],
            "update": progress_update["message"],
            "next_steps": progress_update["next_steps"],
        }


class ProgrammeFundEditProgressUpdate(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/progress_updates/edit_programme_fund.html"
    form_class = ProgrammeFundProgressUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = str(self.kwargs.get("barrier_id"))
        kwargs["programme_fund_update_id"] = str(
            kwargs.pop("progress_update_id", self.kwargs.get("progress_update_id"))
        )
        return kwargs

    def get_initial(self):
        progress_update = next(
            (
                item
                for item in self.barrier.programme_fund_progress_updates
                if item["id"] == str(self.kwargs.get("progress_update_id"))
            ),
            None,
        )
        updates = self.barrier.programme_fund_progress_updates
        progress_update_id = self.kwargs.get("progress_update_id")
        return {
            "milestones_and_deliverables": progress_update[
                "milestones_and_deliverables"
            ],
            "expenditure": progress_update["expenditure"],
        }


class BarrierListProgressUpdate(BarrierMixin, TemplateView):
    template_name = "barriers/progress_updates/list_top_100.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "page": "progress_updates",
                "progress_updates": self.barrier.progress_updates,
            }
        )
        return context_data


class ProgrammeFundListProgressUpdate(BarrierMixin, TemplateView):
    template_name = "barriers/progress_updates/list_programme_fund.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                "page": "progress_updates",
                "progress_updates": self.barrier.programme_fund_progress_updates,
            }
        )
        return context_data
