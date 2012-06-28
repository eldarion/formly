from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required

from formly.forms.run import PageForm
from formly.models import Survey, Field


@login_required
def take_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    page = survey.next_page(user=request.user)
    if page is None: # survey is complete
        return redirect("home")
    
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
        "page": page,
        "form": form
    })
