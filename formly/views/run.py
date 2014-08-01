import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required

from formly.forms.run import PageForm, TargetForm
from formly.models import Survey, Field, FieldChoice
from formly.utils.importing import load_path_attr


COMPLETE_REDIRECT_CALLBACK = load_path_attr(getattr(
    settings,
    "FORMLY_COMPLETE_REDIRECT_CALLBACK",
    "formly.callbacks.survey_complete_redirect"
))


@login_required
def take_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    page = survey.next_page(user=request.user)
    if page is None:  # survey is complete
        return redirect(COMPLETE_REDIRECT_CALLBACK(survey))

    if request.method == "POST":
        kwargs = dict(data=request.POST, page=page)
        if page.fields.filter(field_type=Field.MEDIA_FIELD).exists():
            kwargs.update({"files": request.FILES})

        form = PageForm(**kwargs)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("formly_rt_take_survey", pk=survey.pk)
    else:
        form = PageForm(page=page)

    return render(request, "formly/run/page.html", {
        "survey": survey,
        "page": page,
        "form": form
    })


@login_required
def choice_question(request, pk):
    choice = get_object_or_404(FieldChoice, pk=pk)

    if request.method == "POST":
        kwargs = dict(data=request.POST, choice=choice)
        if choice.target.field_type == Field.MEDIA_FIELD:
            kwargs.update({"files": request.FILES})

        form = TargetForm(**kwargs)
        if form.is_valid():
            form.save(user=request.user)
            form = TargetForm(choice=choice)
    else:
        form = TargetForm(choice=choice)

    data = {
        "html": render_to_string(
            "formly/run/_question.html",
            RequestContext(request, {"form": form}))
    }
    return HttpResponse(json.dumps(data), content_type="application/json")
