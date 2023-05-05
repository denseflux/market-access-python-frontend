import logging

from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView
from utils.api.client import MarketAccessAPIClient
from reports.report_barrier_forms import (
    BarrierNameForm,
    BarrierSummaryForm,
    BarrierReviewForm
)
from django.http import HttpResponseRedirect
from formtools.wizard.views import NamedUrlSessionWizardView, get_storage
from formtools.preview import FormPreview

logger = logging.getLogger(__name__)



class ReportBarrierVanillaWizardView(NamedUrlSessionWizardView, FormPreview):
    form_list = [
        ("barrier-name", BarrierNameForm),
        ("barrier-summary", BarrierSummaryForm),
        ("barrier-review", BarrierReviewForm),
    ]

    def get_template_names(self):
        templates = {
            form_name: f"reports/{form_name.replace('-', '_')}_wizard_step.html"
            for form_name in self.form_list
        }
        return [templates[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):

        submitted_values = {}
        for form in form_list:
            submitted_values = {**submitted_values, **form.clean()}

        client = MarketAccessAPIClient(self.request.session.get("sso_token"))
        new_barrier_report = client.reports.create()

        client.reports.patch(
            id=new_barrier_report.id,
            **submitted_values
        )

        return HttpResponseRedirect(reverse("barriers:dashboard"))












# How draft barriers work;
# Clicking 'Report A Barrier'->'Start' creates a barrier in the DB, it has a status of 0, a code and created/modified dates & creator
# it also has an attribute 'draft' that is set to 't', this is updated to 'f' once all the needed sections are complete
# and the report-a-barrier flow is complete.
# Assume draft list is a list based on querying by user-id and 'draft'='t'

# Docs for formWizard
# https://django-formtools.readthedocs.io/en/latest/wizard.html#advanced-wizardview-methods

# process_step is form_wizard method we can use to update stored draft barrier each time a page-form is submitted
# by getting the input details and calling the MarketAccessAPIClient

# Can't use formpreview with formwizard:
# https://forum.djangoproject.com/t/django-form-wizard-preview-before-submission/5582
# The last form page can be a summary of previously entered values (with links back to previous pages) and done() is called
# on submitting that last page, done method then updates the API by setting 'draft' to 'f'

# Multiple forms in SessionWizard which we can re-call-upon?
# get_context_data? get_form_initial?



class ReportBarrierWizardView(NamedUrlSessionWizardView, FormPreview):

    form_list = [
        ("barrier-name", BarrierNameForm),
        ("barrier-summary", BarrierSummaryForm),
        ("barrier-review", BarrierReviewForm),
    ]




    # When initialising the view, we either get the existing draft, or create a new draft barrier
    # theory; navigating back to this page manually through url bar will take you to the one stored in session,
    # going through the report_a_barrier button (or the draft list) will load into the session the new data
    #
    #_draft_barrier = None

    #@property
    #def draft_barrier(self):
    #    #if not self._draft_barrier:
    #    #    self._draft_barrier = self.get_draft_barrier()
    #    return self._draft_barrier

    def __init__(self, *args, **kwargs):
        super(ReportBarrierWizardView, self).__init__(*args, **kwargs)
        self.draft_barrier = None

    #def get_draft_barrier(self):
    #    client = MarketAccessAPIClient(self.request.session.get("sso_token"))
    #    logger.critical("****************************")
    #    logger.critical("GETTING DRAFT BARRIER:")
    #    logger.critical(self.kwargs)
    #    barrier_id = self.kwargs.get("barrier_id")
#
    #    logger.critical("GOT THE FOLLOWING BARRIER PASSED: " + str(barrier_id))
#
    #    logger.critical("****************************")
#
    #    if barrier_id is None:
    #        # from market-access-api "Barriers are called Reports until they're submitted via self.submit_report()"
    #        # creating a Report object creates a barrier with the bare-minimum of information
    #        return client.reports.create()
    #    else:
    #        return client.reports.get(id=barrier_id)


    def get(self, request, *args, **kwargs):
        """
        This method handles GET requests.

        If a GET request reaches this point, the wizard assumes that the user
        just starts at the first step or wants to restart the process.
        The data of the wizard will be resetted before rendering the first step
        """
        #self.storage.reset()
        # reset the current step to the first step.
        #self.storage.current_step = self.steps.first

        logger.critical("*********************")
        logger.critical("DOING GET")
        logger.critical(str(kwargs))
        
        client = MarketAccessAPIClient(self.request.session.get("sso_token"))
        # Barrier passed in kwarg, we are resuming an existing barrier
        if 'barrier_id' in kwargs.keys():
            self._draft_barrier = client.reports.get(id=kwargs["barrier_id"])
            self.set_existing_barrier_fields(self.draft_barrier)
        # No step or barrier ID passed means we are starting a new barrier
        if 'barrier_id' not in kwargs.keys() and 'step' not in kwargs.keys():
            self.storage.reset()
            # reset the current step to the first step.
            self.storage.current_step = self.steps.first
            #self.draft_barrier = client.reports.create()
            new_barrier_report = client.reports.create()
            request.session['draft_barrier'] = new_barrier_report.id
        # Other scenarios; we're mid flow and alrady have a barrier loaded into self.storage.step_data

        #logger.critical(self.draft_barrier.__dict__)

        #self.storage.extra_data = self._draft_barrier

        logger.critical("-")
        #logger.critical(self.storage.extra_data)
        #logger.critical(self.steps.current)
        #logger.critical(self.steps.prev)
        #logger.critical(self.storage.get_step_data("barrier-name"))
        #logger.critical(self.storage.get_step_data("barrier-summary"))
        logger.critical(request.session['draft_barrier'])


        logger.critical("*********************")
        return self.render(self.get_form())

    def set_existing_barrier_fields(self, barrier):
        # Custom method for us to translate an existing barrier drafts details
        # into field values

        self.storage.set_step_data("barrier-name", {"title": barrier.title})

        self.storage.set_step_data("barrier-summary", {"summary": barrier.summary})


    def get_template_names(self):
        templates = {
            form_name: f"reports/{form_name.replace('-', '_')}_wizard_step.html"
            for form_name in self.form_list
        }
        logger.critical("........................")
        # problem; back button isn't loading the last template
        logger.critical("SELECTING TEMPLATE: " + self.steps.current)
        logger.critical("........................")
        return [templates[self.steps.current]]



    def get_form_initial(self, step):
        """
        Returns a dictionary which will be passed to the form for `step`
        as `initial`. If no initial data was provided while initializing the
        form wizard, an empty dictionary will be returned.
        """

        logger.critical("------------------------------")
        logger.critical("GETTING INITIAL DATA:")
        #logger.critical(self.kwargs)
        logger.critical(self.initial_dict)
        #logger.critical("GOT DRAFT: " + str(self.draft_barrier.__dict__))
        
        self.initial_dict[step] = self.storage.get_step_data(step)
        #self.storage.set_step_data("barrier-name", {"title": barrier.title})
        #self.storage.set_step_data("barrier-summary", {"summary": barrier.summary})



        logger.critical("------------------------------")
        return self.initial_dict.get(step, {})



    #def get_context_data(self, form, **kwargs):
    #    context = super().get_context_data(form=form, **kwargs)
    #    #context.update(self.storage.extra_data)
#
    #    logger.critical("==============================")
    #    logger.critical("GETTING CONTEXT:")
    #    #logger.critical("KWARGS: " + str(kwargs))
    #    #logger.critical(self.storage.get_step_data("barrier-name"))
    #    #logger.critical(self.storage.get_step_data("barrier-summary"))
    #    #logger.critical("GOT DRAFT: " + str(self.draft_barrier.__dict__))
    #    #for line in context:
    #    #    logger.critical(context[line])
#
    #    # can add extra attributes here
    #    #if self.steps.current == 'my_step_name':
    #    #    context.update({'another_var': True})
#
    #    logger.critical("==============================")
    #    return context



    def process_step(self, form):
        """
        This method is used to postprocess the form data. By default, it
        returns the raw `form.data` dictionary.
        """
        logger.critical("+++++++++++++++++++++++++++++++++")
        logger.critical("PROCESSING STEP:")
        #logger.critical(self.__dict__)
        logger.critical(str(self.request.session['draft_barrier']))
        #logger.critical("-")
        logger.critical("-")
        #logger.critical(form.__dict__)

        # Get dictionary of submitted values
        submitted_values = form.clean()

        client = MarketAccessAPIClient(form.token)

        logger.critical(submitted_values)

        client.reports.patch(
            id=self.request.session['draft_barrier'],
            **submitted_values
        )

        logger.critical("+++++++++++++++++++++++++++++++++")
        return self.get_form_step_data(form)


    def done(self, form_list, form_dict, **kwargs):
        #enquiry_subject_cleaned_data = self.get_cleaned_data_for_step("enquiry-subject")
        #enquiry_subject = enquiry_subject_cleaned_data["enquiry_subject"]

        # We call the 'report' function in api to turn the draft into a barrier
        # check convert_to_barrier in market-access-api

        logger.critical("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        logger.critical("DOING THE DONE: ")
        logger.critical("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        return HttpResponseRedirect(reverse("barriers:dashboard"))