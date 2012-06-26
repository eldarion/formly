from django.shortcuts import redirect, render, get_object_or_404

from django.contrib.auth.decorators import login_required

from formly.forms.run import PageForm
from formly.models import Survey


@login_required
def take_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    page = survey.next_page(user=request.user)
    if page is None: # survey is complete
        return redirect("home")
    
    if request.method == "POST":
        form = PageForm(data=request.POST, page=page)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("formly_rt_take_survey", pk=survey.pk)
    else:
        form = PageForm(page=page)
    
    return render(request, "formly/run/page.html", {
        "page": page,
        "form": form
    })
