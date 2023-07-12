from django.urls import path, re_path

from barriers.views.action_plans import (
    ActionPlanMilestoneFormView,
    ActionPlanRisksAndMitigationView,
    ActionPlanStakeholdersListView,
    ActionPlanTaskCompletionDateChangeFormView,
    ActionPlanTaskFormView,
    ActionPlanTemplateView,
    AddActionPlanStrategicContext,
    CreateActionPlanStakeholderIndividualFormView,
    CreateActionPlanStakeholderOrganisationFormView,
    CreateActionPlanStakeholderTypeFormView,
    DeleteActionPlanMilestoneView,
    DeleteActionPlanTaskView,
    EditActionPlanCurrentStatusFormView,
    EditActionPlanOwner,
    EditActionPlanStakeholderDetailsFormView,
    EditActionPlanTaskOutcomeFormView,
    EditActionPlanTaskProgressFormView,
    RemoveActionPlanOwner,
    SelectActionPlanOwner,
)
from barriers.views.light_touch_reviews import (
    PublicBarrierLightTouchReviewsEdit,
    PublicBarrierLightTouchReviewsHMTradeCommissionerApprovalEnabled,
)
from barriers.views.mentions import (
    MentionMarkAllAsRead,
    MentionMarkAllAsUnread,
    MentionMarkAsRead,
    MentionMarkAsReadAndRedirect,
    MentionMarkAsUnread,
    TurnNotificationsOffAndRedirect,
    TurnNotificationsOnAndRedirect,
)
from barriers.views.progress_updates import (
    BarrierAddProgrammeFundProgressUpdate,
    BarrierAddTop100ProgressUpdate,
    BarrierCompleteNextStepItem,
    BarrierEditNextStepItem,
    BarrierEditProgressUpdate,
    BarrierListNextStepsItems,
    BarrierListProgressUpdate,
    ChooseProgressUpdateTypeView,
    ProgrammeFundEditProgressUpdate,
    ProgrammeFundListProgressUpdate,
)

from .views.archive import ArchiveBarrier, UnarchiveBarrier
from .views.assessments.economic import (
    AddEconomicAssessment,
    AddEconomicAssessmentDocument,
    ArchiveEconomicAssessment,
    AutomateEconomicAssessment,
    CancelEconomicAssessmentDocument,
    DeleteEconomicAssessmentDocument,
    EconomicAssessmentDetail,
    EconomicAssessmentRawData,
    EditEconomicAssessmentRating,
)
from .views.assessments.economic_impact import (
    AddEconomicImpactAssessment,
    ArchiveEconomicImpactAssessment,
    EconomicImpactAssessmentDetail,
)
from .views.assessments.overview import AssessmentOverview
from .views.assessments.resolvability import (
    AddResolvabilityAssessment,
    ArchiveResolvabilityAssessment,
    EditResolvabilityAssessment,
    ResolvabilityAssessmentDetail,
)
from .views.assessments.strategic import (
    AddStrategicAssessment,
    ArchiveStrategicAssessment,
    EditStrategicAssessment,
    StrategicAssessmentDetail,
)
from .views.categories import (
    AddCategory,
    BarrierEditCategories,
    BarrierEditCategoriesSession,
    BarrierRemoveCategory,
)
from .views.commodities import BarrierEditCommodities
from .views.companies import (
    BarrierEditCompanies,
    BarrierEditCompaniesSession,
    BarrierRemoveCompany,
    BarrierSearchCompany,
    CompanyDetail,
)
from .views.core import BarrierDetail, Dashboard, WhatIsABarrier
from .views.documents import DownloadDocument
from .views.edit import (
    BarrierEditCausedByTradingBloc,
    BarrierEditCommercialValue,
    BarrierEditEconomicAssessmentEligibility,
    BarrierEditEstimatedResolutionDate,
    BarrierEditEstimatedResolutionDateConfirmationPage,
    BarrierEditPriority,
    BarrierEditProduct,
    BarrierEditSource,
    BarrierEditStartDate,
    BarrierEditSummary,
    BarrierEditTags,
    BarrierEditTerm,
    BarrierEditTitle,
    BarrierEditTradeDirection,
)
from .views.export_types import BarrierEditExportType
from .views.government_organisations import (
    BarrierAddGovernmentOrganisation,
    BarrierEditGovernmentOrganisations,
    BarrierRemoveGovernmentOrganisation,
)
from .views.history import BarrierHistory
from .views.location import (
    AddAdminArea,
    BarrierEditCountryOrTradingBloc,
    BarrierEditLocation,
    BarrierEditLocationSession,
    RemoveAdminArea,
)
from .views.notes import (
    AddNoteDocument,
    BarrierAddNote,
    BarrierDeleteNote,
    BarrierEditNote,
    CancelNoteDocument,
    DeleteNoteDocument,
)
from .views.public_barriers import (
    EditPublicEligibility,
    EditPublicSummary,
    EditPublicTitle,
    PublicBarrierDetail,
    PublicBarrierListView,
)
from .views.saved_searches import (
    DeleteSavedSearch,
    NewSavedSearch,
    RenameSavedSearch,
    SavedSearchNotifications,
)
from .views.search import (
    BarrierSearch,
    DownloadBarriers,
    RequestBarrierDownloadApproval,
)
from .views.sectors import (
    BarrierAddAllSectors,
    BarrierAddMainSector,
    BarrierAddSectors,
    BarrierEditSectors,
    BarrierEditSectorsSession,
    BarrierRemoveSector,
)
from .views.statuses import BarrierChangeStatus
from .views.teams import (
    BarrierTeam,
    ChangeOwnerView,
    DeleteTeamMember,
    SearchTeamMember,
)
from .views.wto import (
    AddWTODocument,
    CancelWTODocuments,
    DeleteWTODocument,
    EditWTOProfile,
    EditWTOStatus,
)

app_name = "barriers"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("search/", BarrierSearch.as_view(), name="search"),
    path("find-a-barrier/", BarrierSearch.as_view(), name="find_a_barrier"),
    path("search/download/", DownloadBarriers.as_view(), name="download"),
    path(
        "search/request_download_approval/",
        RequestBarrierDownloadApproval.as_view(),
        name="request_download_approval",
    ),
    path("what-is-a-barrier/", WhatIsABarrier.as_view(), name="what_is_a_barrier"),
    path(
        "documents/<uuid:document_id>/download/",
        DownloadDocument.as_view(),
        name="download_document",
    ),
    path("saved-searches/new/", NewSavedSearch.as_view(), name="new_saved_search"),
    path(
        "saved-searches/<uuid:saved_search_id>/rename/",
        RenameSavedSearch.as_view(),
        name="rename_saved_search",
    ),
    path(
        "saved-searches/<uuid:saved_search_id>/delete/",
        DeleteSavedSearch.as_view(),
        name="delete_saved_search",
    ),
    path(
        "saved-searches/<uuid:saved_search_id>/notifications/",
        SavedSearchNotifications.as_view(),
        name="saved_search_notifications",
    ),
    re_path(
        "saved-searches/(?P<saved_search_id>(my|team)-barriers)/notifications/",
        SavedSearchNotifications.as_view(),
        name="saved_search_notifications",
    ),
    path("barriers/<uuid:barrier_id>/", BarrierDetail.as_view(), name="barrier_detail"),
    # Reason for double url: Analytics requested a second url pointing to the same page
    path(
        "barriers/<uuid:barrier_id>/complete/",
        BarrierDetail.as_view(),
        name="barrier_detail_from_complete",
    ),
    re_path(
        "barriers/(?P<barrier_id>[A-Z]-[0-9]{2}-[A-Z0-9]{3})/",
        BarrierDetail.as_view(),
        name="barrier_detail_by_code",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/title/",
        BarrierEditTitle.as_view(),
        name="edit_title",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/product/",
        BarrierEditProduct.as_view(),
        name="edit_product",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/summary/",
        BarrierEditSummary.as_view(),
        name="edit_summary",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/source/",
        BarrierEditSource.as_view(),
        name="edit_source",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/priority/",
        BarrierEditPriority.as_view(),
        name="edit_priority",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/term/",
        BarrierEditTerm.as_view(),
        name="edit_term",
    ),
    path(
        "barriers/<uuid:barrier_id>/list/top_100_progress_update/",
        BarrierListProgressUpdate.as_view(),
        name="list_top_100_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/top_100_progress_update/<uuid:progress_update_id>/",
        BarrierEditProgressUpdate.as_view(),
        name="edit_top_100_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/list/programme_fund_progress_update/",
        ProgrammeFundListProgressUpdate.as_view(),
        name="list_barrier_fund_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/programme_fund_progress_update/<uuid:progress_update_id>/",
        ProgrammeFundEditProgressUpdate.as_view(),
        name="edit_barrier_fund_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/list/next_steps_items/",
        BarrierListNextStepsItems.as_view(),
        name="list_next_steps",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/next_step_item_update/<uuid:item_id>/",
        BarrierEditNextStepItem.as_view(),
        name="edit_next_steps",
    ),
    path(
        "barriers/<uuid:barrier_id>/add/next_step_item_update/",
        BarrierEditNextStepItem.as_view(),
        name="add_next_steps",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/next_step_item_complete/<uuid:item_id>/",
        BarrierCompleteNextStepItem.as_view(),
        name="complete_next_steps",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/economic-assessment-eligibility/",
        BarrierEditEconomicAssessmentEligibility.as_view(),
        name="economic_assessment_eligibility",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/estimated-resolution-date/",
        BarrierEditEstimatedResolutionDate.as_view(),
        name="edit_estimated_resolution_date",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/estimated-resolution-date/confirmation/",
        BarrierEditEstimatedResolutionDateConfirmationPage.as_view(),
        name="edit_estimated_resolution_date_confirmation_page",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/commercial-value/",
        BarrierEditCommercialValue.as_view(),
        name="edit_commercial_value",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/commodities/",
        BarrierEditCommodities.as_view(),
        name="edit_commodities",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/commodities/<str:mode>/",
        BarrierEditCommodities.as_view(),
        name="edit_commodities_sr",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/tags/",
        BarrierEditTags.as_view(),
        name="edit_tags",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/trade-direction/",
        BarrierEditTradeDirection.as_view(),
        name="edit_trade_direction",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/caused-by-trading-bloc/",
        BarrierEditCausedByTradingBloc.as_view(),
        name="edit_caused_by_trading_bloc",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/wto-status/",
        EditWTOStatus.as_view(),
        name="edit_wto_status",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/wto/",
        EditWTOProfile.as_view(),
        name="edit_wto_profile",
    ),
    path(
        "barriers/<uuid:barrier_id>/wto/documents/add/",
        AddWTODocument.as_view(),
        name="add_wto_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/wto/documents/cancel/",
        CancelWTODocuments.as_view(),
        name="cancel_wto_documents",
    ),
    path(
        "barriers/<uuid:barrier_id>/wto/documents/<uuid:document_id>/delete/",
        DeleteWTODocument.as_view(),
        name="delete_wto_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/archive/", ArchiveBarrier.as_view(), name="archive"
    ),
    path(
        "barriers/<uuid:barrier_id>/unarchive/",
        UnarchiveBarrier.as_view(),
        name="unarchive",
    ),
    path(
        "barriers/<uuid:barrier_id>/history/", BarrierHistory.as_view(), name="history"
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/add-note/",
        BarrierAddNote.as_view(),
        name="add_note",
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/edit-note/<int:note_id>/",
        BarrierEditNote.as_view(),
        name="edit_note",
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/delete-note/<int:note_id>/",
        BarrierDeleteNote.as_view(),
        name="delete_note",
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/documents/add/",
        AddNoteDocument.as_view(),
        name="add_note_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/documents/cancel/",
        CancelNoteDocument.as_view(),
        name="cancel_note_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/interactions/documents/<uuid:document_id>/delete/",
        DeleteNoteDocument.as_view(),
        name="delete_note_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/location/",
        BarrierEditLocationSession.as_view(),
        name="edit_location_session",
    ),
    path(
        "barriers/<uuid:barrier_id>/location/edit/",
        BarrierEditLocation.as_view(),
        name="edit_location",
    ),
    path(
        "barriers/<uuid:barrier_id>/location/country/",
        BarrierEditCountryOrTradingBloc.as_view(),
        name="edit_country",
    ),
    path(
        "barriers/<uuid:barrier_id>/location/add-admin-area/",
        AddAdminArea.as_view(),
        name="add_admin_area",
    ),
    path(
        "barriers/<uuid:barrier_id>/location/remove-admin-area/",
        RemoveAdminArea.as_view(),
        name="remove_admin_area",
    ),
    path(
        "barriers/<uuid:barrier_id>/status/",
        BarrierChangeStatus.as_view(),
        name="change_status",
    ),
    path(
        "barriers/<uuid:barrier_id>/types/",
        BarrierEditCategoriesSession.as_view(),
        name="edit_categories_session",
    ),
    path(
        "barriers/<uuid:barrier_id>/types/edit/",
        BarrierEditCategories.as_view(),
        name="edit_categories",
    ),
    path(
        "barriers/<uuid:barrier_id>/types/remove/",
        BarrierRemoveCategory.as_view(),
        name="remove_category",
    ),
    path(
        "barriers/<uuid:barrier_id>/types/add/",
        AddCategory.as_view(),
        name="add_category",
    ),
    path(
        "barriers/<uuid:barrier_id>/sectors/",
        BarrierEditSectorsSession.as_view(),
        name="edit_sectors_session",
    ),
    path(
        "barriers/<uuid:barrier_id>/sectors/edit/",
        BarrierEditSectors.as_view(),
        name="edit_sectors",
    ),
    path(
        "barriers/<uuid:barrier_id>/sectors/remove/",
        BarrierRemoveSector.as_view(),
        name="remove_sector",
    ),
    path(
        "barriers/<uuid:barrier_id>/sectors/add/",
        BarrierAddSectors.as_view(),
        name="add_sectors",
    ),
    path(
        "barriers/<uuid:barrier_id>/main-sector/add/",
        BarrierAddMainSector.as_view(),
        name="add_main_sector",
    ),
    path(
        "barriers/<uuid:barrier_id>/sectors/add/all/",
        BarrierAddAllSectors.as_view(),
        name="add_all_sectors",
    ),
    path(
        "barriers/<uuid:barrier_id>/government-organisations/edit/",
        BarrierEditGovernmentOrganisations.as_view(),
        name="edit_gov_orgs",
    ),
    path(
        "barriers/<uuid:barrier_id>/government-organisations/remove/",
        BarrierRemoveGovernmentOrganisation.as_view(),
        name="remove_gov_orgs",
    ),
    path(
        "barriers/<uuid:barrier_id>/government-organisations/add/",
        BarrierAddGovernmentOrganisation.as_view(),
        name="add_gov_orgs",
    ),
    path(
        "barriers/<uuid:barrier_id>/companies/",
        BarrierEditCompaniesSession.as_view(),
        name="edit_companies_session",
    ),
    path(
        "barriers/<uuid:barrier_id>/companies/edit/",
        BarrierEditCompanies.as_view(),
        name="edit_companies",
    ),
    path(
        "barriers/<uuid:barrier_id>/companies/search/",
        BarrierSearchCompany.as_view(),
        name="search_company",
    ),
    path(
        "barriers/<uuid:barrier_id>/companies/remove/",
        BarrierRemoveCompany.as_view(),
        name="remove_company",
    ),
    path(
        "barriers/<uuid:barrier_id>/companies/<str:company_id>/",
        CompanyDetail.as_view(),
        name="company_detail",
    ),
    path("barriers/<uuid:barrier_id>/team/", BarrierTeam.as_view(), name="team"),
    path(
        "barriers/<uuid:barrier_id>/team/add/search/",
        SearchTeamMember.as_view(),
        name="search_team_member",
    ),
    path(
        "barriers/<uuid:barrier_id>/team/delete/<int:team_member_id>",
        DeleteTeamMember.as_view(),
        name="delete_team_member",
    ),
    path(
        "barriers/<uuid:barrier_id>/team/change-owner/<int:team_member_id>",
        ChangeOwnerView.as_view(),
        name="team_change_owner",
    ),
    path(
        "barriers/<uuid:barrier_id>/assessments/",
        AssessmentOverview.as_view(),
        name="assessment_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/add",
        AddEconomicAssessment.as_view(),
        name="add_economic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/automate",
        AutomateEconomicAssessment.as_view(),
        name="automate_economic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/add-rating",
        EditEconomicAssessmentRating.as_view(),
        name="add_economic_assessment_rating",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/",
        EconomicAssessmentDetail.as_view(),
        name="economic_assessment_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/raw-data",
        EconomicAssessmentRawData.as_view(),
        name="economic_assessment_raw_data",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/edit/rating",
        EditEconomicAssessmentRating.as_view(),
        name="edit_economic_assessment_rating",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/archive",
        ArchiveEconomicAssessment.as_view(),
        name="archive_economic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/documents/add/",
        AddEconomicAssessmentDocument.as_view(),
        name="add_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/documents/cancel/",
        CancelEconomicAssessmentDocument.as_view(),
        name="cancel_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/documents/<uuid:document_id>/delete/",
        DeleteEconomicAssessmentDocument.as_view(),
        name="delete_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/documents/add/",
        AddEconomicAssessmentDocument.as_view(),
        name="add_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/documents/cancel/",
        CancelEconomicAssessmentDocument.as_view(),
        name="cancel_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-assessments/<int:assessment_id>/documents/<uuid:document_id>/delete/",
        DeleteEconomicAssessmentDocument.as_view(),
        name="delete_economic_assessment_document",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-impact-assessments/add",
        AddEconomicImpactAssessment.as_view(),
        name="add_economic_impact_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-impact-assessments/<uuid:assessment_id>/",
        EconomicImpactAssessmentDetail.as_view(),
        name="economic_impact_assessment_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/economic-impact-assessments/<uuid:assessment_id>/archive",
        ArchiveEconomicImpactAssessment.as_view(),
        name="archive_economic_impact_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/resolvability-assessments/add",
        AddResolvabilityAssessment.as_view(),
        name="add_resolvability_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/resolvability-assessments/<uuid:assessment_id>/",
        ResolvabilityAssessmentDetail.as_view(),
        name="resolvability_assessment_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/resolvability-assessments/<uuid:assessment_id>/edit",
        EditResolvabilityAssessment.as_view(),
        name="edit_resolvability_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/resolvability-assessments/<uuid:assessment_id>/archive",
        ArchiveResolvabilityAssessment.as_view(),
        name="archive_resolvability_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/strategic-assessments/add",
        AddStrategicAssessment.as_view(),
        name="add_strategic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan",
        ActionPlanTemplateView.as_view(),
        name="action_plan",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/edit_current_status",
        EditActionPlanCurrentStatusFormView.as_view(),
        name="action_plan_edit_current_status",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/add_risks_and_mitigations",
        ActionPlanRisksAndMitigationView.as_view(),
        name="action_plan_add_risks_and_mitigations",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/stakeholders/",
        ActionPlanStakeholdersListView.as_view(),
        name="action_plan_stakeholders_list",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/stakeholders/new/",
        CreateActionPlanStakeholderTypeFormView.as_view(),
        name="action_plan_stakeholders_add",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/stakeholders/new/individual/",
        CreateActionPlanStakeholderIndividualFormView.as_view(),
        name="action_plan_stakeholders_new_individual",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/stakeholders/new/organisation/",
        CreateActionPlanStakeholderOrganisationFormView.as_view(),
        name="action_plan_stakeholders_new_organisation",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/stakeholders/<uuid:id>/",
        EditActionPlanStakeholderDetailsFormView.as_view(),
        name="action_plan_stakeholders_edit",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/edit_owner",
        SelectActionPlanOwner.as_view(),
        name="action_plan_edit_owner",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/remove_owner",
        RemoveActionPlanOwner.as_view(),
        name="action_plan_remove_owner",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/existing_owner",
        EditActionPlanOwner.as_view(),
        name="action_plan_edit_existing_owner",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/add_strategic_context",
        AddActionPlanStrategicContext.as_view(),
        name="action_plan_add_strategic_context",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/new/",
        ActionPlanMilestoneFormView.as_view(),
        name="action_plan_add_milestone",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:id>/",
        ActionPlanMilestoneFormView.as_view(),
        name="action_plan_edit_milestone",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:milestone_id>/delete_milestone",
        DeleteActionPlanMilestoneView.as_view(),
        name="action_plan_delete_milestone",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:milestone_id>/tasks/new/",
        ActionPlanTaskFormView.as_view(),
        name="action_plan_add_task",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:milestone_id>/tasks/<uuid:id>/",
        ActionPlanTaskFormView.as_view(),
        name="action_plan_edit_task",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:milestone_id>/tasks/<uuid:id>/check-start_date/",
        ActionPlanTaskCompletionDateChangeFormView.as_view(),
        name="action_plan_completion_date_change",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/<uuid:id>/edit_outcome",
        EditActionPlanTaskOutcomeFormView.as_view(),
        name="action_plan_edit_outcome",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/<uuid:id>/edit_progress",
        EditActionPlanTaskProgressFormView.as_view(),
        name="action_plan_edit_progress",
    ),
    path(
        "barriers/<uuid:barrier_id>/action_plan/milestones/<uuid:milestone_id>/tasks/<uuid:task_id>/delete_task",
        DeleteActionPlanTaskView.as_view(),
        name="action_plan_delete_task",
    ),
    path(
        "barriers/<uuid:barrier_id>/strategic-assessments/<uuid:assessment_id>/",
        StrategicAssessmentDetail.as_view(),
        name="strategic_assessment_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/strategic-assessments/<uuid:assessment_id>/edit",
        EditStrategicAssessment.as_view(),
        name="edit_strategic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/strategic-assessments/<uuid:assessment_id>/archive",
        ArchiveStrategicAssessment.as_view(),
        name="archive_strategic_assessment",
    ),
    path(
        "barriers/<uuid:barrier_id>/public/",
        PublicBarrierDetail.as_view(),
        name="public_barrier_detail",
    ),
    path(
        "barriers/<uuid:barrier_id>/public/eligibility/",
        EditPublicEligibility.as_view(),
        name="edit_public_eligibility",
    ),
    path(
        "barriers/<uuid:barrier_id>/public/title/",
        EditPublicTitle.as_view(),
        name="edit_public_barrier_title",
    ),
    path(
        "barriers/<uuid:barrier_id>/public/summary/",
        EditPublicSummary.as_view(),
        name="edit_public_barrier_summary",
    ),
    path(
        "barriers/<uuid:barrier_id>/mark_approved",
        PublicBarrierLightTouchReviewsEdit.as_view(),
        name="edit_public_barrier_reviews",
    ),
    path(
        "barriers/<uuid:barrier_id>/enable_hm_trade_commissioner_approvals",
        PublicBarrierLightTouchReviewsHMTradeCommissionerApprovalEnabled.as_view(),
        name="enable_hm_trade_commissioner_approvals",
    ),
    path(
        "barriers/<uuid:barrier_id>/progress_updates/for",
        ChooseProgressUpdateTypeView.as_view(),
        name="choose_progress_update_type",
    ),
    path(
        "barriers/<uuid:barrier_id>/progress_updates/top_100_priority",
        BarrierAddTop100ProgressUpdate.as_view(),
        name="add_top_100_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/progress_updates/programme_fund",
        BarrierAddProgrammeFundProgressUpdate.as_view(),
        name="add_programme_fund_progress_update",
    ),
    path(
        "barriers/<uuid:barrier_id>/edit/start-date/",
        BarrierEditStartDate.as_view(),
        name="edit_start_date",
    ),
    path(
        "barriers/<uuid:barrier_id>/export-types/edit/",
        BarrierEditExportType.as_view(),
        name="edit_export_types",
    ),
    path("public-barriers/", PublicBarrierListView.as_view(), name="public_barriers"),
    path(
        "mentions/mark-as-read/<int:mention_id>",
        MentionMarkAsRead.as_view(),
        name="mention_mark_as_read",
    ),
    path(
        "mentions/mark-as-unread/<int:mention_id>",
        MentionMarkAsUnread.as_view(),
        name="mention_mark_as_unread",
    ),
    path(
        "mentions/go-to/<int:mention_id>",
        MentionMarkAsReadAndRedirect.as_view(),
        name="mention_go_to",
    ),
    path(
        "mentions/mark-all-as-read/",
        MentionMarkAllAsRead.as_view(),
        name="mention_mark_all_as_read",
    ),
    path(
        "mentions/mark-all-as-unread/",
        MentionMarkAllAsUnread.as_view(),
        name="mention_mark_all_as_unread",
    ),
    path(
        "mentions/turn-notifications-off",
        TurnNotificationsOffAndRedirect.as_view(),
        name="mention_turn_notifications_off",
    ),
    path(
        "mentions/turn-notifications-on",
        TurnNotificationsOnAndRedirect.as_view(),
        name="mention_turn_notifications_on",
    ),
]
