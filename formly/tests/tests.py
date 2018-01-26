from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ..models import Field, FieldChoice, Survey

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

    def test_multiplechoice_field_choice_limit(self):
        """
        Enforce maximum_choices on multiple choice fields that allow
        multiple answers.
        """
        survey = Survey.objects.create(
            name="multiple choice test",
            creator=self.user,
        )
        field = Field.objects.create(
            survey=survey,
            label="multiple choice field",
            field_type=Field.CHECKBOX_FIELD,
            maximum_choices=1,
            ordinal=0,
        )
        choice_pks = []
        for label in ["a", "b"]:
            choice = FieldChoice.objects.create(label=label, field=field)
            choice_pks.append(choice.pk)

        form_field = field.form_field()
        with self.assertRaises(ValidationError):
            form_field.clean(choice_pks)
