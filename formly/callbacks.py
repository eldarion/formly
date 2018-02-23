from django.urls import reverse


def survey_complete_redirect(survey):
    return reverse("home")
