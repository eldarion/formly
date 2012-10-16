from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required

from formly.forms.run import PageForm
from formly.models import Survey, Field
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
