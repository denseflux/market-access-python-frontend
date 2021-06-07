from barriers.forms.action_plans import (ActionPlanMilestoneEditForm,
                                         ActionPlanMilestoneForm,
                                         ActionPlanTaskEditForm,
                                         ActionPlanTaskForm)
from barriers.views.mixins import APIBarrierFormViewMixin, BarrierMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, TemplateView
from utils.api.client import MarketAccessAPIClient


class AddActionPlanMilestoneFormView(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/action_plans/add_milestone.html"
    form_class = ActionPlanMilestoneForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        return kwargs

    def get_success_url(self):
        return reverse(
            "barriers:action_plan", kwargs={"barrier_id": self.kwargs.get("barrier_id")}
        )


class EditActionPlanMilestoneFormView(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/action_plans/edit_milestone.html"
    form_class = ActionPlanMilestoneEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        kwargs["milestone_id"] = self.kwargs.get("id")
        return kwargs

    def get_milestone(self):
        milestones = self.action_plan.milestones
        found = list(
            filter(
                lambda milestone: milestone["id"] == str(self.kwargs.get("id")),
                milestones,
            )
        )
        return found[0]

    def get_initial(self):
        if self.request.method == "GET":
            return self.get_milestone()

    def get_success_url(self):
        return reverse(
            "barriers:action_plan", kwargs={"barrier_id": self.kwargs.get("barrier_id")}
        )


class DeleteActionPlanMilestoneView(View):
    def get(self, request, *args, **kwargs):
        client = MarketAccessAPIClient(self.request.session.get("sso_token"))
        milestone_id = str(self.kwargs.get("id"))
        barrier_id = str(self.kwargs.get("barrier_id"))
        client.action_plans.delete_milestone(barrier_id, milestone_id)
        return HttpResponseRedirect(
            reverse(
                "barriers:action_plan",
                kwargs={"barrier_id": self.kwargs.get("barrier_id")},
            )
        )


class AddActionPlanTaskFormView(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/action_plans/add_task.html"
    form_class = ActionPlanTaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        kwargs["action_plan_id"] = self.request.GET.get("action_plan")
        kwargs["milestone_id"] = self.request.GET.get("milestone")
        return kwargs

    def get_success_url(self):
        return reverse(
            "barriers:action_plan", kwargs={"barrier_id": self.kwargs.get("barrier_id")}
        )


class EditActionPlanTaskFormView(APIBarrierFormViewMixin, FormView):
    template_name = "barriers/action_plans/edit_task.html"
    form_class = ActionPlanTaskEditForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["token"] = self.request.session.get("sso_token")
        kwargs["barrier_id"] = self.kwargs.get("barrier_id")
        kwargs["action_plan_id"] = self.request.GET.get("action_plan")
        kwargs["milestone_id"] = self.request.GET.get("milestone")
        kwargs["task_id"] = self.kwargs.get("id")
        return kwargs

    def get_task(self):
        milestones = self.action_plan.milestones
        for milestone in milestones:
            for task in milestone["tasks"]:
                if task["id"] == str(self.kwargs.get("id")):
                    return {**task, "assigned_to": task["assigned_to_email"]}

    def get_initial(self):
        if self.request.method == "GET":
            return self.get_task()

    def get_success_url(self):
        return reverse(
            "barriers:action_plan", kwargs={"barrier_id": self.kwargs.get("barrier_id")}
        )


class DeleteActionPlanTaskView(View):
    def get(self, request, *args, **kwargs):
        client = MarketAccessAPIClient(self.request.session.get("sso_token"))
        task_id = str(self.kwargs.get("id"))
        barrier_id = str(self.kwargs.get("barrier_id"))
        client.action_plans.delete_task(barrier_id, task_id)
        return HttpResponseRedirect(
            reverse(
                "barriers:action_plan",
                kwargs={"barrier_id": self.kwargs.get("barrier_id")},
            )
        )


class ActionPlanTemplateView(BarrierMixin, TemplateView):
    template_name = "barriers/action_plans/detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["action_plan"] = self.action_plan
        return context_data
