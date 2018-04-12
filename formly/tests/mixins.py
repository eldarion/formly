from test_plus.test import TestCase

from formly.tests.factories import (
    FieldChoiceFactory,
    FieldFactory,
    FieldResultFactory,
    OrdinalChoiceFactory,
    OrdinalScaleFactory,
    PageFactory,
    SurveyFactory,
    SurveyResultFactory,
)


class TestHelperMixin(object):
    """
    Provides test helper methods
    """
    def _ordinal_scale(self, **kwargs):
        return OrdinalScaleFactory.create(**kwargs)

    def _ordinal_choice(self, create=True, **kwargs):
        """
        Create an ordinal choice. Requires `score` kwarg.
        """
        if "scale" not in kwargs:
            kwargs["scale"] = self.scale
        if create is True:
            return OrdinalChoiceFactory.create(**kwargs)
        else:
            return OrdinalChoiceFactory.build(**kwargs)

    def _survey(self, **kwargs):
        """Create a Survey"""
        if "user" not in kwargs:
            kwargs["user"] = self.user
        return SurveyFactory.create(**kwargs)

    def _surveyresult(self, **kwargs):
        """Create a SurveyResult"""
        if "user" not in kwargs:
            kwargs["user"] = self.user
        return SurveyResultFactory.create(**kwargs)

    def _page(self, create=True, **kwargs):
        if "survey" not in kwargs:
            kwargs["survey"] = self.survey
        if create is True:
            return PageFactory.create(**kwargs)
        else:
            return PageFactory.build(**kwargs)

    def _field(self, create=True, **kwargs):
        if "survey" not in kwargs:
            kwargs["survey"] = self.survey
        if create is True:
            return FieldFactory.create(**kwargs)
        else:
            return FieldFactory.build(**kwargs)

    def _fieldchoice(self, create=True, **kwargs):
        if "field" not in kwargs:
            kwargs["field"] = self.field
        if create is True:
            return FieldChoiceFactory.create(**kwargs)
        else:
            return FieldChoiceFactory.build(**kwargs)

    def _fieldresult(self, create=True, **kwargs):
        """Create a SurveyResult"""
        if "question" not in kwargs:
            kwargs["question"] = self.field
        if create is True:
            return FieldResultFactory.create(**kwargs)
        else:
            return FieldResultFactory.build(**kwargs)


class SimpleTests(TestCase, TestHelperMixin):
    pass
