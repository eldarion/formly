import json

from ..models import Field, FieldChoice, OrdinalScale, Page, Survey
from .mixins import SimpleTests


class ViewTests(SimpleTests):

    def setUp(self):
        self.user = self.make_user("test_user")

    def test_survey_list_authenticated(self):
        """Verify authenticated user can see survey list"""
        survey1 = self._survey()
        survey2 = self._survey()
        with self.login(self.user):
            self.get("formly:survey_list")
            self.response_200()
            self.assertInContext("surveys")
            surveys = self.context["surveys"]
            self.assertSetEqual(set(surveys), {survey1, survey2})

    def test_survey_list_anonymous(self):
        """Verify anonymous user is redirected"""
        self.get("formly:survey_list")
        self.response_302()

    def test_survey_detail_creator(self):
        """Verify survey creator can see survey list"""
        survey1 = self._survey()
        survey2 = self._survey()
        with self.login(self.user):
            self.get("formly:survey_detail", pk=survey1.pk)
            self.response_200()
            surveys = self.context["surveys"]
            self.assertSetEqual(set(surveys), {survey1, survey2})
            selected = self.context["selected_survey"]
            self.assertEqual(selected, survey1)

    def test_survey_detail_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        with self.login(not_creator):
            self.get("formly:survey_detail", pk=survey.pk)
            self.response_403()

    def test_page_detail_creator(self):
        """Verify survey creator can see page detail"""
        self.survey = self._survey()
        page1 = self._page()
        page2 = self._page()  # Create another page for good measure
        with self.login(self.user):
            self.get("formly:page_detail", pk=page1.pk)
            self.response_200()
            pages = self.context["pages"]
            self.assertSetEqual(set(pages), {page1, page2})
            selected = self.context["selected_page"]
            self.assertEqual(selected, page1)

    def test_page_detail_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        self._page()  # Create another page for good measure
        with self.login(not_creator):
            self.get("formly:page_detail", pk=page.pk)
            self.response_403()

    def test_survey_create_authenticated_get(self):
        """Verify authenticated user can access survey creation"""
        with self.login(self.user):
            self.get("formly:survey_create")
            self.response_200()
            self.assertInContext("form")

    def test_survey_create_anonymous_get(self):
        """Verify anonymous user is redirected"""
        self.get("formly:survey_create")
        self.response_302()

    def test_survey_create_post(self):
        """Verify authenticated user can create a survey"""
        survey_name = "Excellent Survey"
        post_data = {
            "name": survey_name
        }
        with self.login(self.user):
            self.post("formly:survey_create", data=post_data)
            self.response_302()
            survey = Survey.objects.get(name=survey_name)
            self.assertEqual(survey.creator, self.user)

    def test_survey_change_name_creator(self):
        """Verify survey creator can change survey name"""
        survey = self._survey()
        survey_name = "Excellent Survey"
        post_data = {
            "name": survey_name
        }
        with self.login(self.user):
            self.post("formly:survey_change_name", pk=survey.pk, data=post_data)
            self.response_200()
            self.assertTrue(Survey.objects.get(name=survey_name))
            json_data = json.loads(self.last_response.content.decode("utf-8"))
            self.assertEqual(json_data["status"], "OK")
            self.assertEqual(json_data["name"], survey_name)

    def test_survey_change_name_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        with self.login(not_creator):
            self.post("formly:survey_change_name", pk=survey.pk)
            self.response_403()

    def test_survey_change_name_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:survey_change_name", pk=55)
        self.response_302()

    def test_survey_publish_creator(self):
        """Verify survey creator can publish survey"""
        survey = self._survey()
        self.assertFalse(survey.published)
        with self.login(self.user):
            self.post("formly:survey_publish", pk=survey.pk)
            self.response_302()
            survey.refresh_from_db()
            self.assertTrue(survey.published)

    def test_survey_publish_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        with self.login(not_creator):
            self.post("formly:survey_publish", pk=survey.pk)
            self.response_403()

    def test_survey_publish_anonymous(self):
        """Verify anonymous user is redirected"""
        survey = self._survey()
        self.post("formly:survey_publish", pk=survey.pk)
        self.response_302()
        self.assertFalse(survey.published)

    def test_survey_duplicate_creator(self):
        """Verify survey creator can publish survey"""
        survey = self._survey()
        page1 = self._page(survey=survey)
        field1 = self._field(survey=survey, page=page1)
        self._fieldchoice(field=field1)
        self._fieldchoice(field=field1)
        field2 = self._field(survey=survey, page=page1)
        self._fieldchoice(field=field2)
        self._fieldchoice(field=field2)
        page2 = self._page(survey=survey)
        self._field(survey=survey, page=page2)
        self._field(survey=survey, page=page2)
        with self.login(self.user):
            self.post("formly:survey_duplicate", pk=survey.pk, follow=True)
            self.response_200()
            selected = self.context["selected_survey"]
            self.assertNotEqual(selected.pk, survey.pk)
            self.assertEqual(selected.name, survey.name)

    def test_survey_duplicate_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        with self.login(not_creator):
            self.post("formly:survey_duplicate", pk=survey.pk)
            self.response_403()

    def test_survey_duplicate_anonymous(self):
        """Verify anonymous user is redirected"""
        survey = self._survey()
        self.post("formly:survey_duplicate", pk=survey.pk)
        self.response_302()
        self.assertFalse(survey.published)

    def test_page_create_anonymous_post(self):
        """Verify anonymous user is redirected"""
        self.post("formly:page_create", pk=55)
        self.response_302()

    def test_page_create_post(self):
        """Verify authenticated user can create a survey"""
        survey = self._survey()
        with self.login(self.user):
            self.post("formly:page_create", pk=survey.pk, follow=True)
            page = Page.objects.get(survey=survey)
            self.assertRedirects(self.last_response, page.get_absolute_url())

    def test_page_create_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        with self.login(not_creator):
            self.post("formly:page_create", pk=survey.pk)
            self.response_403()

    def test_field_create_anonymous_post(self):
        """Verify anonymous user is redirected"""
        self.post("formly:field_create", pk=55)
        self.response_302()

    def test_field_create_post(self):
        """Verify authenticated user can create a field"""
        survey = self._survey()
        page = self._page(survey=survey)
        with self.login(self.user):
            self.post("formly:field_create", pk=page.pk, follow=True)
            field = Field.objects.get(page=page, survey=survey)
            self.assertRedirects(self.last_response, field.get_absolute_url())
            self.assertEqual(field.label, "New Field")
            self.assertEqual(field.field_type, Field.TEXT_FIELD)
            self.assertEqual(field.ordinal, 1)

    def test_field_create_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        survey = self._survey()
        page = self._page(survey=survey)
        with self.login(not_creator):
            self.post("formly:field_create", pk=page.pk)
            self.response_403()

    def test_page_update_creator_get(self):
        """Verify survey creator is allowed"""
        self.survey = self._survey()
        page1 = self._page()
        with self.login(self.user):
            self.get("formly:page_update", pk=page1.pk)
            self.response_200()
            page = self.context["page"]
            self.assertEqual(page, page1)
            self.assertTrue(self.context["form"])

    def test_page_update_not_creator_get(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        self._page()  # Create another page for good measure
        with self.login(not_creator):
            self.get("formly:page_update", pk=page.pk)
            self.response_403()

    def test_page_update_page_update(self):
        """Verify survey creator can update page"""
        self.survey = self._survey()
        page1 = self._page()
        post_data = dict(
            action="page_update",
            subtitle="Submarine Title",
        )
        with self.login(self.user):
            self.post("formly:page_update", pk=page1.pk, data=post_data, follow=True)
            page = self.context["selected_page"]
            self.assertRedirects(self.last_response, page.get_absolute_url())
            self.assertEqual(page.subtitle, post_data["subtitle"])

    def test_page_update_add_field(self):
        """Verify survey creator can add field to page"""
        self.survey = self._survey()
        page1 = self._page()
        post_data = {
            "action": "field_add",
            "fields-label": "Field Hockey",
            "fields-field_type": Field.TEXT_FIELD,
            "fields-expected_answers": 1,
        }
        with self.login(self.user):
            self.post("formly:page_update", pk=page1.pk, data=post_data, follow=True)
            page = self.context["selected_page"]
            self.assertRedirects(self.last_response, page.get_absolute_url())
            self.assertTrue(
                Field.objects.get(label=post_data["fields-label"], survey=self.survey, page=page1)
            )

    def test_field_move_up_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(not_creator):
            self.post("formly:field_move_up", pk=field.pk)
            self.response_403()

    def test_field_move_up_anonymous_post(self):
        """Verify anonymous user is redirected"""
        self.post("formly:field_move_up", pk=55)
        self.response_302()

    def test_field_move_up(self):
        """Verify survey creator can move a field up"""
        self.survey = self._survey()
        page = self._page()
        field1 = self._field(page=page, ordinal=1)
        field2 = self._field(page=page, ordinal=2)
        with self.login(self.user):
            self.post("formly:field_move_up", pk=field2.pk)
        field1.refresh_from_db()
        field2.refresh_from_db()
        self.assertTrue(field2.ordinal < field1.ordinal)

    def test_field_move_down_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(not_creator):
            self.post("formly:field_move_down", pk=field.pk)
            self.response_403()

    def test_field_move_down_anonymous_post(self):
        """Verify anonymous user is redirected"""
        self.post("formly:field_move_down", pk=55)
        self.response_302()

    def test_field_move_down(self):
        """Verify survey creator can move a field down"""
        self.survey = self._survey()
        page = self._page()
        field1 = self._field(page=page, ordinal=1)
        field2 = self._field(page=page, ordinal=2)
        with self.login(self.user):
            self.post("formly:field_move_down", pk=field1.pk)
        field1.refresh_from_db()
        field2.refresh_from_db()
        self.assertTrue(field2.ordinal < field1.ordinal)

    def test_survey_results_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        survey = self._survey()
        not_creator = self.make_user("not_creator")
        with self.login(not_creator):
            self.get("formly:survey_results", pk=survey.pk)
            self.response_403()

    def test_survey_results(self):
        """Verify survey creator can obtain survey results"""
        survey = self._survey()
        with self.login(self.user):
            self.get("formly:survey_results", pk=survey.pk)
            self.assertTemplateUsed(template_name="formly/results/home.html")

    def test_remap_answer_get(self):
        survey = self._survey()
        page = self._page(survey=survey)
        surveyresult = self._surveyresult(survey=survey)
        field = self._field(
            page=page,
            survey=survey,
            field_type=Field.MULTIPLE_TEXT,
            expected_answers=4
        )
        fieldresult = self._fieldresult(
            survey=survey,
            question=field,
            answer={"answer": ["thing", "thiing", "thang", "tang"]},
            page=page,
            result=surveyresult
        )

        with self.login(self.user):
            self.get(
                "formly:survey_results_remap",
                pk=fieldresult.pk,
                answer_string="thing",
            )
            self.assertTemplateUsed(template_name="formly/results/remap.html")

    def test_remap_answer_post(self):
        survey = self._survey()
        page = self._page(survey=survey)
        surveyresult = self._surveyresult(survey=survey)
        field = self._field(page=page, survey=survey, field_type=Field.MULTIPLE_TEXT, expected_answers=4)
        fieldresult = self._fieldresult(
            survey=survey,
            question=field,
            answer={"answer": ["thing", "thiing", "thang", "tang"]},
            page=page,
            result=surveyresult
        )
        with self.login(self.user):
            post_data = {
                "mapping": ["thiing"]
            }
            self.post(
                "formly:survey_results_remap",
                pk=fieldresult.pk,
                answer_string="thing",
                data=post_data,
            )
            self.response_302()

    def test_remap_answer_post_ajax(self):
        survey = self._survey()
        page = self._page(survey=survey)
        surveyresult = self._surveyresult(survey=survey)
        field = self._field(page=page, survey=survey, field_type=Field.MULTIPLE_TEXT, expected_answers=4)
        fieldresult = self._fieldresult(
            survey=survey,
            question=field,
            answer={"answer": ["thing", "thiing", "thang", "tang"]},
            page=page,
            result=surveyresult
        )
        with self.login(self.user):
            post_data = {
                "mapping": ["thiing"]
            }
            self.post(
                "formly:survey_results_remap",
                pk=fieldresult.pk,
                answer_string="thing",
                data=post_data,
                extra={
                    "HTTP_X_REQUESTED_WITH": "XMLHttpRequest"
                }
            )
            self.response_200()

    def test_field_add_choice_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(not_creator):
            self.post("formly:field_add_choice", pk=field.pk)
            self.response_403()

    def test_field_add_choice(self):
        """Verify survey creator can add field choice"""
        self.survey = self._survey()
        page1 = self._page()
        field1 = self._field(page=page1)
        post_data = {
            "choices-label": "New Field Choice!"
        }
        original_choices = FieldChoice.objects.count()
        with self.login(self.user):
            self.post("formly:field_add_choice", pk=field1.pk, data=post_data, follow=True)
            self.assertRedirects(self.last_response, field1.get_absolute_url())
            self.assertEqual(FieldChoice.objects.count(), original_choices + 1)

    def test_field_add_choice_bad_data(self):
        """Verify survey creator sees expected response with bad POST data"""
        self.survey = self._survey()
        page1 = self._page()
        field1 = self._field(page=page1)
        post_data = {
            "nothing": "New Field Choice!"
        }
        with self.login(self.user):
            self.post("formly:field_add_choice", pk=field1.pk, data=post_data)
            self.response_200()
            self.assertTemplateUsed(template_name="formly/design/survey_list.html")

    def test_likert_scale_set_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:ajax_likert_scale_set", field_pk=55, scale_pk=56)
        self.response_302()

    def test_likert_scale_set(self):
        """Verify authenticated user can set a field ordinal scale"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.LIKERT_FIELD)
        scale = self._ordinal_scale(kind=OrdinalScale.ORDINAL_KIND_LIKERT)
        self.assertFalse(field.scale)  # ensure no scale associated
        with self.login(self.user):
            self.post("formly:ajax_likert_scale_set", field_pk=field.pk, scale_pk=scale.pk)
        field.refresh_from_db()
        self.assertEqual(field.scale, scale)
        self.assertTemplateUsed(template_name="formly/design/_likert_scales.html")

    def test_likert_scale_create_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:ajax_likert_scale_create", field_pk=55)
        self.response_302()

    def test_likert_scale_create(self):
        """Verify authenticated user can create a field ordinal scale"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.LIKERT_FIELD)
        self.assertFalse(field.scale)  # ensure no scale associated
        post_data = dict(
            name="Tiny Scale",
            scale="1,2,3",
        )
        with self.login(self.user):
            self.post("formly:ajax_likert_scale_create", field_pk=field.pk, data=post_data)
        field.refresh_from_db()
        self.assertTrue(field.scale)
        self.assertEqual(field.scale.kind, OrdinalScale.ORDINAL_KIND_LIKERT)
        self.assertTemplateUsed(template_name="formly/design/_likert_scale_form.html")
        self.assertTemplateUsed(template_name="formly/design/_likert_scales.html")

    def test_rating_scale_set_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:ajax_rating_scale_set", field_pk=55, scale_pk=56)
        self.response_302()

    def test_rating_scale_set(self):
        """Verify authenticated user can set a field ordinal scale"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.RATING_FIELD)
        scale = self._ordinal_scale(kind=OrdinalScale.ORDINAL_KIND_RATING)
        self.assertFalse(field.scale)  # ensure no scale associated
        with self.login(self.user):
            self.post("formly:ajax_rating_scale_set", field_pk=field.pk, scale_pk=scale.pk)
        field.refresh_from_db()
        self.assertEqual(field.scale, scale)
        self.assertTemplateUsed(template_name="formly/design/_rating_scales.html")

    def test_rating_scale_create_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:ajax_rating_scale_create", field_pk=55)
        self.response_302()

    def test_rating_scale_create(self):
        """Verify authenticated user can create a field ordinal scale"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.RATING_FIELD)
        self.assertFalse(field.scale)  # ensure no scale associated
        post_data = dict(
            name="Bigger Scale",
            scale="1,2,3,4,5,6",
        )
        with self.login(self.user):
            self.post("formly:ajax_rating_scale_create", field_pk=field.pk, data=post_data)
        field.refresh_from_db()
        self.assertTrue(field.scale)
        self.assertEqual(field.scale.kind, OrdinalScale.ORDINAL_KIND_RATING)
        self.assertTemplateUsed(template_name="formly/design/_rating_scale_form.html")
        self.assertTemplateUsed(template_name="formly/design/_rating_scales.html")

    def test_field_update_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:field_update", pk=55)
        self.response_302()

    def test_field_update_bad_data(self):
        """Verify expected response when POST data is bad/incomplete"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.RATING_FIELD)
        post_data = dict(
            field_type=Field.TEXT_FIELD,
            expected_answers=1,
        )
        with self.login(self.user):
            self.post("formly:field_update", pk=field.pk, data=post_data)
            self.response_200()
            self.assertTemplateUsed(template_name="formly/design/survey_list.html")

    def test_field_update(self):
        """Verify field is updated as expected"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page, field_type=Field.RATING_FIELD)
        post_data = dict(
            action="field_update",
            label="Field Hockey",
            field_type=Field.TEXT_FIELD,
            expected_answers=1,
        )
        with self.login(self.user):
            self.post("formly:field_update", pk=field.pk, data=post_data)
            self.assertRedirects(self.last_response, field.get_absolute_url())

    def test_field_update_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(not_creator):
            self.post("formly:field_update", pk=field.pk)
            self.response_403()

    def test_choice_delete_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:ajax_choice_delete", pk=55)
        self.response_302()

    def test_choice_delete_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        with self.login(not_creator):
            self.post("formly:ajax_choice_delete", pk=choice.pk)
            self.response_403()

    def test_choice_delete(self):
        """Verify survey creator can delete field choice"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        self.assertIn(choice, field.choices.all())
        self.assertEqual(field.choices.count(), 1)
        with self.login(self.user):
            self.post("formly:ajax_choice_delete", pk=choice.pk)
            self.response_200()
            self.assertFalse(field.choices.all())

    def test_choice_update_anonymous(self):
        """Verify anonymous user is redirected"""
        self.post("formly:choice_update", pk=55)
        self.response_302()

    def test_choice_update_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        with self.login(not_creator):
            self.post("formly:choice_update", pk=choice.pk)
            self.response_403()

    def test_choice_update_get(self):
        """Verify survey creator can access field choice update"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        with self.login(self.user):
            self.get("formly:choice_update", pk=choice.pk)
            self.response_200()
            self.assertTemplateUsed(template_name="formly/design/choice_form.html")

    def test_choice_update(self):
        """Verify survey creator can update field choice"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        post_data = dict(
            label="New Choice",
        )
        with self.login(self.user):
            self.post("formly:choice_update", pk=choice.pk, data=post_data)
            choice.refresh_from_db()
            self.assertEqual(choice.label, post_data["label"])

    def test_survey_delete_view(self):
        """Verify survey creator can delete survey"""
        self.survey = self._survey()
        with self.login(self.user):
            self.post("formly:survey_delete", pk=self.survey.pk)
            self.assertFalse(Survey.objects.count())

    def test_survey_delete_view_not_creator(self):
        """Verify user who didn't create survey is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        with self.login(not_creator):
            self.post("formly:survey_delete", pk=self.survey.pk)
            self.response_403()

    def test_page_delete_view(self):
        """Verify survey creator can delete survey"""
        self.survey = self._survey()
        page = self._page()
        with self.login(self.user):
            self.post("formly:page_delete", pk=page.pk)
            self.assertFalse(Page.objects.count())

    def test_page_delete_view_not_creator(self):
        """Verify user who didn't create page is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        with self.login(not_creator):
            self.post("formly:page_delete", pk=page.pk)
            self.response_403()

    def test_field_delete_view(self):
        """Verify survey creator can delete survey"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(self.user):
            self.post("formly:field_delete", pk=field.pk)
            self.assertFalse(Field.objects.count())

    def test_field_delete_view_not_creator(self):
        """Verify user who didn't create field is not allowed"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        with self.login(not_creator):
            self.post("formly:field_delete", pk=field.pk)
            self.response_403()

    def test_choice_delete_view(self):
        """Verify survey creator can delete survey"""
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        with self.login(self.user):
            self.post("formly:choice_delete", pk=choice.pk)
            self.assertFalse(FieldChoice.objects.count())

    def test_choice_delete_view_not_creator(self):
        """Verify survey creator can delete survey"""
        not_creator = self.make_user("not_creator")
        self.survey = self._survey()
        page = self._page()
        field = self._field(page=page)
        choice = self._fieldchoice(field=field)
        with self.login(not_creator):
            self.post("formly:choice_delete", pk=choice.pk)
            self.response_403()

    def test_take_survey(self):
        self.survey = self._survey()
        page1 = self._page()
        field1 = self._field(page=page1)
        page2 = self._page()
        field2 = self._field(page=page2)
        survey_taker = self.make_user("survey_taker")
        with self.login(survey_taker):
            # Start the survey
            self.get("formly:take_survey", pk=self.survey.pk)

            # Post answers to first page
            post_data = {
                "{}".format(field1.name): "Five",
            }
            self.post("formly:take_survey", pk=self.survey.pk, data=post_data)
            self.assertRedirects(self.last_response, self.survey.get_run_url())

            # Post answers to second page
            post_data = {
                "{}".format(field2.name): "Six",
            }
            self.post("formly:take_survey", pk=self.survey.pk, data=post_data)
            self.response_302()
            self.assertEqual(field1.results.get().answer, {"answer": "Five"})
            self.assertEqual(field2.results.get().answer, {"answer": "Six"})
