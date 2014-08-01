from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

from formly.models import Survey


@login_required
def survey_results(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.view_results", obj=survey):
        raise PermissionDenied()

    return render(request, "formly/results/home.html", {
        "survey": survey,
    })
