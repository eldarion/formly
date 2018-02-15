import factory
from formly.models import OrdinalChoice, OrdinalScale, Page, Survey


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


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page
