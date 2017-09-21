from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import (
    Field,
    Survey,
)

User = get_user_model()


class Tests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user("foo", password="bar")

    def test_likert_field_missing_scale(self):
        """
        Ensure Likert field missing choices still produces form field.
        """
        survey = Survey(
            name="likert test",
            creator=self.user,
        )
        # create Likert field without associated LikertScale
        field = Field(
            survey=survey,
            label="likert field",
            field_type=Field.LIKERT_FIELD,
        )
        self.assertFalse(field.choices.all())
        # Ensure no exception when field has no choices
        self.assertTrue(field.form_field())

    def test_text_field_form_field_render(self):
        survey = Survey(
            name="field mapping test",
            creator=self.user,
        )
        field = Field(
            survey=survey,
            label="text field",
            field_type=Field.TEXT_FIELD,
        )
        # Ensure no exception when field is instantiated
        self.assertTrue(field.form_field())
