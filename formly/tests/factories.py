import factory

from formly.models import (
    Field,
    FieldChoice,
    FieldResult,
    OrdinalChoice,
    OrdinalScale,
    Page,
    Survey,
    SurveyResult,
)


class OrdinalChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrdinalChoice

    label = factory.Sequence(lambda n: "label-{}".format(n))


class OrdinalScaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrdinalScale

    name = factory.Sequence(lambda n: "scale-{}".format(n))
    kind = OrdinalScale.ORDINAL_KIND_RATING


class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey

    class Params:
        user = None

    name = factory.Sequence(lambda n: "survey-{}".format(n))
    creator = factory.LazyAttribute(lambda o: o.user)


class SurveyResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SurveyResult


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page


class FieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Field

    label = factory.Sequence(lambda n: "field-label-{}".format(n))
    field_type = Field.TEXT_FIELD
    ordinal = factory.Sequence(lambda n: n)


class FieldChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FieldChoice

    label = factory.Sequence(lambda n: "choice-label-{}".format(n))


class FieldResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FieldResult
