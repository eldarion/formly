from django.conf.urls import url

from formly.views import design
from formly.views import results
from formly.views import run

app_name = "formly"


urlpatterns = [
    url(r"^design/$", design.survey_list, name="dt_survey_list"),
    url(r"^design/surveys/(?P<pk>\d+)/$", design.survey_detail, name="dt_survey_detail"),
    url(r"^design/surveys/create/$", design.survey_create, name="dt_survey_create"),
    url(r"^design/surveys/(?P<pk>\d+)/change-name/$", design.survey_change_name, name="dt_survey_change_name"),
    url(r"^design/surveys/(?P<pk>\d+)/duplicate/$", design.survey_duplicate, name="dt_survey_duplicate"),
    url(r"^design/surveys/(?P<pk>\d+)/publish/$", design.survey_publish, name="dt_survey_publish"),
    url(r"^design/surveys/(?P<pk>\d+)/pages/create/$", design.page_create, name="_dt_page_create"),
    url(r"^design/pages/(?P<pk>\d+)/$", design.page_detail, name="dt_page_detail"),
    url(r"^design/pages/(?P<pk>\d+)/fields/create/$", design.fields_create, name="dt_field_create"),
    url(r"^design/pages/(?P<pk>\d+)/update/$", design.page_update, name="dt_page_update"),
    url(r"^design/fields/(?P<pk>\d+)/update/$", design.field_update, name="dt_field_update"),
    url(r"^design/fields/(?P<pk>\d+)/choices/add/$", design.field_add_choice, name="dt_field_add_choice"),
    url(r"^design/fields/(?P<pk>\d+)/move-up/$", design.field_move_up, name="dt_field_move_up"),
    url(r"^design/fields/(?P<pk>\d+)/move-down/$", design.field_move_down, name="dt_field_move_down"),
    url(r"^design/choices/(?P<pk>\d+)/update/$", design.choice_update, name="dt_choice_update"),
    url(r"^design/fields/(?P<pk>\d+)/delete/$", design.FieldDeleteView.as_view(), name="dt_field_delete"),
    url(r"^design/choices/(?P<pk>\d+)/delete/$", design.ChoiceDeleteView.as_view(), name="dt_choice_delete"),
    url(r"^design/pages/(?P<pk>\d+)/delete/$", design.PageDeleteView.as_view(), name="dt_page_delete"),
    url(r"^design/surveys/(?P<pk>\d+)/delete/$", design.SurveyDeleteView.as_view(), name="dt_survey_delete"),

    url(r"^ajax/design/choices/(?P<pk>\d+)/delete/$", design.choice_delete, name="dt_ajax_choice_delete"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/likert-scales/(?P<scale_pk>\d+)/set/$", design.likert_scale_set, name="dt_ajax_likert_scale_set"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/likert-scales/create/$", design.likert_scale_create, name="dt_ajax_likert_scale_create"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/rating-scales/(?P<scale_pk>\d+)/set/$", design.rating_scale_set, name="dt_ajax_rating_scale_set"),
    url(r"^ajax/design/fields/(?P<field_pk>\d+)/rating-scales/create/$", design.rating_scale_create, name="dt_ajax_rating_scale_create"),

    url(r"^run/survey/(?P<pk>\d+)/$", run.take_survey, name="rt_take_survey"),
    url(r"^run/ajax/choice-question/(?P<pk>\d+)/$", run.choice_question, name="rt_choice_question"),

    url(r"^results/survey/(?P<pk>\d+)/$", results.survey_results, name="survey_results"),
]
