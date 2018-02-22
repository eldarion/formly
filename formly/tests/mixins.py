from test_plus.test import TestCase

from formly.tests.factories import (
    FieldFactory,
    OrdinalChoiceFactory,
    OrdinalScaleFactory,
    PageFactory,
    SurveyFactory,
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

class SimpleTests(TestCase, TestHelperMixin):
    pass
