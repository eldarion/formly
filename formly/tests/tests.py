from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from formly.forms.run import PageForm

from ..models import (
    Field,
    Survey,
    FieldChoice,
    Page,
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

    def test_multiplechoice_field_choice_form_widgets(self):

        survey = Survey.objects.create(
            name="choice widget test",
            creator=self.user,
        )

        page = Page.objects.create(
            survey=survey,
            page_num=1,
            subtitle="Single page survey",
        )

        field1 = Field.objects.create(
            survey=survey,
            label="multiple choice field1",
            field_type=Field.CHECKBOX_FIELD,
            maximum_choices=1,
            ordinal=0,
            page=page,
        )
        field2 = Field.objects.create(
            survey=survey,
            label="multiple choice field2",
            field_type=Field.CHECKBOX_FIELD,
            maximum_choices=1,
            ordinal=0,
            page=page,
        )

        choice_pks = []
        for label in ["a", "b"]:
            choice = FieldChoice.objects.create(label=label, field=field1)
            choice_pks.append(choice.pk)

        for label in ["c", "d"]:
            choice = FieldChoice.objects.create(label=label, field=field2)
            choice_pks.append(choice.pk)

        form = PageForm(page=page)
        form_htm = form.as_p()

        # The form should have all four key values for all four fields
        for c_pk in choice_pks:
            self.assertTrue('value="{}"'.format(c_pk) in form_htm)
