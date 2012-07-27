import json

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from formly.utils.views import BaseDeleteView
from formly.forms.design import SurveyCreateForm, PageUpdateForm, FieldForm, FieldChoiceForm
from formly.models import Survey, Page, Field, FieldChoice


@login_required
def survey_list(request):
    unpublished_surveys = Survey.objects.filter(published__isnull=True)
    published_surveys = Survey.objects.filter(published__isnull=False)
    
    if not request.user.has_perm("formly.view_survey_list"):
        raise PermissionDenied()
    
    return render(request, "formly/design/survey_list.html", {
        "unpublished_surveys": unpublished_surveys,
        "published_surveys": published_surveys
    })


@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    if not request.user.has_perm("formly.view_survey_detail", obj=survey):
        raise PermissionDenied()
    
    return render(request, "formly/design/survey_detail.html", {
        "survey": survey,
    })


@login_required
def survey_create(request):
    if not request.user.has_perm("formly.create_survey"):
        raise PermissionDenied()
    
    if request.method == "POST":
        form = SurveyCreateForm(request.POST, user=request.user)
        if form.is_valid():
            survey = form.save()
            return redirect(survey.first_page())
    else:
        form = SurveyCreateForm(user=request.user)
    
    return render(request, "formly/design/survey_form.html", {
        "form": form,
    })


@require_POST
@login_required
def survey_change_name(request, pk):
    """
    Works well with:
      http://www.appelsiini.net/projects/jeditable
    """
    survey = get_object_or_404(Survey, pk=pk)
    
    if not request.user.has_perm("formly.change_survey_name", obj=survey):
        raise PermissionDenied()
    
    survey.name = request.POST.get("name")
    survey.save()
    return HttpResponse(json.dumps({
        "status": "OK",
        "name": survey.name
    }), mimetype="application/json")


@require_POST
@login_required
def survey_publish(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    if not request.user.has_perm("formly.publish_survey", obj=survey):
        raise PermissionDenied()
    
    survey.publish()
    return redirect("formly_dt_survey_list")


@require_POST
@login_required
def survey_duplicate(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    if not request.user.has_perm("formly.duplicate_survey", obj=survey):
        raise PermissionDenied()
    
    duped = survey.duplicate()
    return redirect("formly_dt_survey_detail", pk=duped.pk)


@require_POST
@login_required
def page_create(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=survey):
        raise PermissionDenied()
    
    page = survey.pages.create()
    return redirect(page)


@login_required
def page_update(request, pk):
    page = get_object_or_404(Page, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=page.survey):
        raise PermissionDenied()
    
    if request.method == "POST":
        if request.POST.get("action") == "page_update":
            form = PageUpdateForm(data=request.POST, instance=page)
            field_form = FieldForm(prefix="fields")
            if form.is_valid():
                page = form.save()
                return redirect(page)
        if request.POST.get("action") == "field_add":
            form = PageUpdateForm(instance=page)
            field_form = FieldForm(request.POST, prefix="fields")
            if field_form.is_valid():
                field = field_form.save(commit=False)
                field.page = page
                field.survey = page.survey
                field.save()
                return redirect(page)
    else:
        form = PageUpdateForm(instance=page)
        field_form = FieldForm(prefix="fields")
    return render(request, "formly/design/page_form.html", {
        "form": form,
        "page": page,
        "field_form": field_form
    })


@require_POST
@login_required
def field_move_up(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()
    
    field.move_up()
    return HttpResponse(json.dumps({
        "status": "OK",
        "ordinal": field.ordinal,
        "location": reverse("formly_dt_page_update", kwargs={"pk": field.page.pk})
    }), mimetype="application/json")


@require_POST
@login_required
def field_move_down(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()
    
    field.move_down()
    return HttpResponse(json.dumps({
        "status": "OK",
        "ordinal": field.ordinal,
        "location": reverse("formly_dt_page_update", kwargs={"pk": field.page.pk})
    }), mimetype="application/json")


@login_required
def field_update(request, pk):
    field = get_object_or_404(Field, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()
    
    if request.method == "POST":
        if request.POST.get("action") == "field_update":
            form = FieldForm(data=request.POST, instance=field)
            field_choice_form = FieldChoiceForm(field=field, prefix="choices")
            if form.is_valid():
                form.save()
                return redirect(field.page.get_absolute_url())
        if request.POST.get("action") == "choice_add":
            form = FieldForm(instance=field)
            field_choice_form = FieldChoiceForm(
                data=request.POST,
                field=field,
                prefix="choices"
            )
            if field_choice_form.is_valid():
                choice = field_choice_form.save(commit=False)
                choice.field = field
                choice.save()
                return redirect("formly_dt_field_update", pk=field.pk)
    else:
        form = FieldForm(instance=field)
        field_choice_form = FieldChoiceForm(field=field, prefix="choices")
    
    return render(request, "formly/design/field_form.html", {
        "form": form,
        "page": field.page,
        "field": field,
        "field_choice_form": field_choice_form
    })


@login_required
def choice_update(request, pk):
    choice = get_object_or_404(FieldChoice, pk=pk)
    
    if not request.user.has_perm("formly.edit_survey", obj=choice.field.survey):
        raise PermissionDenied()
    
    if request.method == "POST":
        form = FieldChoiceForm(
            field=choice.field,
            data=request.POST,
            instance=choice
        )
        if form.is_valid():
            form.save()
            return redirect(choice.field.page)
    else:
        form = FieldChoiceForm(field=choice.field, instance=choice)
    
    return render(request, "formly/design/choice_form.html", {
        "form": form,
        "choice": choice,
        "page": choice.field.page
    })


class SurveyDeleteView(BaseDeleteView):
    model = Survey
    success_url_name = "formly_dt_survey_list"


class PageDeleteView(BaseDeleteView):
    model = Page
    success_url_name = "formly_dt_survey_detail"
    pk_obj_name = "survey"


class FieldDeleteView(BaseDeleteView):
    model = Field
    success_url_name = "formly_dt_page_update"
    pk_obj_name = "page"


class ChoiceDeleteView(BaseDeleteView):
    model = FieldChoice
    success_url_name = "formly_dt_field_update"
    pk_obj_name = "field"
