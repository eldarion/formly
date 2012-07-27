from django.core.urlresolvers import reverse


def survey_complete_redirect(survey):
    return reverse("home")
