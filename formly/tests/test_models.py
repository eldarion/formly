import datetime

from django.core.exceptions import ValidationError
from django.urls import reverse

from mock import patch

from .mixins import SimpleTests


class ModelTests(SimpleTests):

    def setUp(self):
        self.user = self.make_user("test_user")
        self.scale = self._ordinal_scale()

    def test_ordinal_scale(self):
        """Ensure proper string representation"""
        choices = [("last", 3), ("middle", 2), ("first", 1)]
        for choice in choices:
            self._ordinal_choice(label=choice[0], score=choice[1])

        expected = "{} [first (1), middle (2), last (3)]".format(self.scale.name)
        self.assertEqual(str(self.scale), expected)

    def test_ordinal_scale_unique_label(self):
        """Ensure scale and choice label uniqueness is enforced"""
        label = "label"
        score = 1
        self._ordinal_choice(label=label, score=score)

        # duplicate label
        choice = self._ordinal_choice(label=label, score=score + 1, create=False)
        msg = "Ordinal choice with this Scale and Label already exists."
        with self.assertRaisesMessage(ValidationError, msg):
            choice.validate_unique()

    def test_ordinal_scale_unique_score(self):
        """Ensure scale and choice score uniqueness is enforced"""
        label = "label"
        score = 1
        self._ordinal_choice(label=label, score=score)

        # duplicate score
        choice = self._ordinal_choice(label="different", score=score, create=False)
        msg = "Ordinal choice with this Scale and Score already exists."
        with self.assertRaisesMessage(ValidationError, msg):
            choice.validate_unique()

    def test_survey_url(self):
        """Verify proper URL"""
        survey = self._survey()
        self.assertEqual(
            survey.get_absolute_url(),
            reverse("formly:survey_detail", args=[survey.pk])
        )

    @patch("formly.models.timezone.now")
    def test_survey_save_updated(self, mock_now):
        """Verify `updated` field is updated on save"""
        fake_now = datetime.datetime(2018, 2, 14)
        mock_now.return_value = datetime.datetime(2018, 2, 14)
        survey = self._survey()
        survey.name = "updated name"
        survey.save()
        self.assertEqual(survey.updated, fake_now)

    def test_page_unspecified_page_num(self):
        """Ensure `page_num` is set as expected"""
        self.survey = self._survey()
        self._page(page_num=2)
        self._page(page_num=1)
        page = self._page()
        self.assertEqual(page.page_num, 3)

    def test_page_label(self):
        """Ensure correct label"""
        self.survey = self._survey()
        page = self._page(page_num=5, create=False)
        # no subtitle, check for default label
        self.assertEqual(page.label(), "Page {}".format(page.page_num))
        # set subtitle
        subtitle = "subtitle"
        page.subtitle = subtitle
        self.assertEqual(page.label(), subtitle)

    def test_page_url(self):
        """Verify proper URL"""
        self.survey = self._survey()
        page = self._page()
        self.assertEqual(
            page.get_absolute_url(),
            reverse("formly:page_detail", args=[page.pk])
        )

    def test_field_move_up(self):
        self.survey = self._survey()
        page1 = self._page()
        field1 = self._field(page=page1, ordinal=1)
        field2 = self._field(page=page1, ordinal=2)
        field2.move_up()
        field1.refresh_from_db()
        field2.refresh_from_db()
        self.assertTrue(field2.ordinal < field1.ordinal)

    def test_field_move_down(self):
        self.survey = self._survey()
        page1 = self._page()
        field1 = self._field(page=page1, ordinal=1)
        field2 = self._field(page=page1, ordinal=2)
        field1.move_down()
        field1.refresh_from_db()
        field2.refresh_from_db()
        self.assertTrue(field2.ordinal < field1.ordinal)
