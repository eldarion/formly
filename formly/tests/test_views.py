import json

from .mixins import SimpleTests
from ..models import Survey


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
        self._survey()
        self._survey()
        self.get("formly:survey_list")
        self.response_302()

    def test_survey_detail_creator(self):
        """Verify authenticated survey creator can see survey list"""
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
        """Verify authenticated survey creator can see survey list"""
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
        """Verify survey creator can change name"""
        survey = self._survey()
        survey_name = "Excellent Survey"
        post_data = {
            "name": survey_name
        }
        with self.login(self.user):
            self.post("formly:survey_change_name", pk=survey.pk, data=post_data)
            self.response_200()
            self.assertTrue(Survey.objects.get(name=survey_name))
            json_data = json.loads(self.last_response.content)
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
        survey = self._survey()
        survey_name = "Excellent Survey"
        post_data = {
            "name": survey_name
        }
        self.post("formly:survey_change_name", pk=survey.pk, data=post_data)
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
        self.assertFalse(survey.published)
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
