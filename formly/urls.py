from django.conf.urls import url

from formly.views import design, results, run

app_name = "formly"


urlpatterns = [
    url(r"^design/$", design.survey_list, name="survey_list"),
    url(r"^design/surveys/(?P<pk>\d+)/$", design.survey_detail, name="survey_detail"),
    url(r"^design/surveys/create/$", design.survey_create, name="survey_create"),
    url(r"^design/surveys/(?P<pk>\d+)/change-name/$", design.survey_change_name, name="survey_change_name"),
    url(r"^design/surveys/(?P<pk>\d+)/duplicate/$", design.survey_duplicate, name="survey_duplicate"),
    url(r"^design/surveys/(?P<pk>\d+)/publish/$", design.survey_publish, name="survey_publish"),
    url(r"^design/surveys/(?P<pk>\d+)/pages/create/$", design.page_create, name="page_create"),
    url(r"^design/pages/(?P<pk>\d+)/$", design.page_detail, name="page_detail"),
    url(r"^design/pages/(?P<pk>\d+)/fields/create/$", design.field_create, name="field_create"),
    url(r"^design/pages/(?P<pk>\d+)/update/$", design.page_update, name="page_update"),
    url(r"^design/fields/(?P<pk>\d+)/update/$", design.field_update, name="field_update"),
    url(r"^design/fields/(?P<pk>\d+)/choices/add/$", design.field_add_choice, name="field_add_choice"),
    url(r"^design/fields/(?P<pk>\d+)/move-up/$", design.field_move_up, name="field_move_up"),
    url(r"^design/fields/(?P<pk>\d+)/move-down/$", design.field_move_down, name="field_move_down"),
    url(r"^design/choices/(?P<pk>\d+)/update/$", design.choice_update, name="choice_update"),
    url(r"^design/fields/(?P<pk>\d+)/delete/$", design.FieldDelete.as_view(), name="field_delete"),
    url(r"^design/choices/(?P<pk>\d+)/delete/$", design.ChoiceDelete.as_view(), name="choice_delete"),
    url(r"^design/pages/(?P<pk>\d+)/delete/$", design.PageDelete.as_view(), name="page_delete"),
    url(r"^design/surveys/(?P<pk>\d+)/delete/$", design.SurveyDelete.as_view(), name="survey_delete"),

    url(r"^ajax/design/choices/(?P<pk>\d+)/delete/$", design.choice_delete, name="ajax_choice_delete"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/likert-scales/(?P<scale_pk>\d+)/set/$", design.likert_scale_set, name="ajax_likert_scale_set"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/likert-scales/create/$", design.likert_scale_create, name="ajax_likert_scale_create"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/rating-scales/(?P<scale_pk>\d+)/set/$", design.rating_scale_set, name="ajax_rating_scale_set"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/rating-scales/create/$", design.rating_scale_create, name="ajax_rating_scale_create"),

    url(r"^run/survey/(?P<pk>\d+)/$", run.take_survey, name="take_survey"),
    url(r"^run/ajax/choice-question/(?P<pk>\d+)/$", run.choice_question, name="choice_question"),

    url(r"^results/survey/(?P<pk>\d+)/$", results.survey_results, name="survey_results"),
    url(r"^results/remap/(?P<pk>\d+)/(?P<answer_string>[\w\W]+)/$", results.RemapView.as_view(), name="survey_results_remap"),
]
