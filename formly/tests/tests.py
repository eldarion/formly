from django.contrib.auth.models import User
from django.test import TestCase

from ..models import (
    Field,
    Survey,
)


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
