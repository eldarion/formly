import json

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required

from formly.utils.views import BaseDeleteView
from formly.forms.design import SurveyCreateForm, PageUpdateForm, FieldForm, FieldChoiceForm, LikertScaleForm
from formly.models import Survey, Page, Field, FieldChoice, LikertScale


@login_required
def survey_list(request):
    if not request.user.has_perm("formly.view_survey_list"):
        raise PermissionDenied()

    return render(request, "formly/design/survey_list.html", {
        "surveys": Survey.objects.all().order_by("-created"),
        "survey_form": SurveyCreateForm(user=request.user)
    })


@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.view_survey_detail", obj=survey):
        raise PermissionDenied()

    return render(request, "formly/design/survey_list.html", {
        "surveys": Survey.objects.all().order_by("-created"),
        "survey_form": SurveyCreateForm(user=request.user),
        "pages": survey.pages.all(),
        "selected_survey": survey
    })


@login_required
def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk)

    if not request.user.has_perm("formly.view_survey_detail", obj=page.survey):
        raise PermissionDenied()

    return render(request, "formly/design/survey_list.html", {
        "surveys": Survey.objects.all().order_by("-created"),
        "survey_form": SurveyCreateForm(user=request.user),
        "pages": page.survey.pages.all(),
        "selected_page": page,
        "selected_survey": page.survey,
        "fields": page.fields.all().order_by("ordinal")
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


@require_POST
@login_required
def fields_create(request, pk):
    page = get_object_or_404(Page, pk=pk)

    if not request.user.has_perm("formly.edit_survey", obj=page.survey):
        raise PermissionDenied()

    field = page.fields.create(
        label="New Field",
        survey=page.survey,
        field_type=Field.TEXT_FIELD,
        ordinal=1
    )

    return redirect(field)


@login_required
def page_update(request, pk):
    # @@@ break this apart into seperate views
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

    data = {
        "html": render_to_string(
            "formly/design/_fields.html",
            {
                "selected_page": field.page,
                "fields": field.page.fields.all().order_by("ordinal"),
                "selected_field": field
            },
            request
        )
    }
    return JsonResponse(data)


@require_POST
@login_required
def field_move_down(request, pk):
    field = get_object_or_404(Field, pk=pk)

    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()

    field.move_down()

    data = {
        "html": render_to_string(
            "formly/design/_fields.html",
            {
                "selected_page": field.page,
                "fields": field.page.fields.all().order_by("ordinal"),
                "selected_field": field
            },
            request
        )
    }
    return JsonResponse(data)


@require_POST
@login_required
def field_add_choice(request, pk):
    field = get_object_or_404(Field, pk=pk)

    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()

    field_choice_form = FieldChoiceForm(
        data=request.POST,
        prefix="choices"
    )
    if field_choice_form.is_valid():
        choice = field_choice_form.save(commit=False)
        choice.field = field
        choice.save()
        return redirect(field)
    form = FieldForm(instance=field)
    return render(request, "formly/design/survey_list.html", {
        "surveys": Survey.objects.all().order_by("-created"),
        "survey_form": SurveyCreateForm(user=request.user),
        "pages": field.page.survey.pages.all(),
        "selected_page": field.page,
        "selected_survey": field.survey,
        "fields": field.page.fields.all().order_by("ordinal"),
        "selected_field": field,
        "field_form": form,
        "field_choice_form": field_choice_form
    })


@require_POST
@login_required
def likert_scale_set(request, field_pk, scale_pk):
    field = get_object_or_404(Field, pk=field_pk, field_type=Field.LIKERT_FIELD)
    scale = get_object_or_404(LikertScale, pk=scale_pk)
    field.scale = scale
    field.save()
    return JsonResponse({
        "html": render_to_string("formly/design/_likert_scales.html", {"selected_field": field, "likert_scales": LikertScale.objects.all()}, request)
    })


@require_POST
@login_required
def likert_scale_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, field_type=Field.LIKERT_FIELD)
    likert_scale_form = LikertScaleForm(request.POST)
    if likert_scale_form.is_valid():
        scale = likert_scale_form.save()
        choices = likert_scale_form.cleaned_data["scale"]
        for index, scale_choice in enumerate(scale.choices.all().order_by("score")):
            if index < len(choices):
                scale_choice.label = choices[index]
                scale_choice.save()
        field.scale = scale
        field.save()
        likert_scale_form = LikertScaleForm()
    return JsonResponse({
        "html": render_to_string("formly/design/_likert_scale_form.html", {"selected_field": field, "likert_scale_form": likert_scale_form}, request),
        "fragments": {
            ".likert-scales": render_to_string("formly/design/_likert_scales.html", {"selected_field": field, "likert_scales": LikertScale.objects.all()}, request)
        }
    })


@login_required
def field_update(request, pk):
    field = get_object_or_404(Field, pk=pk)

    if not request.user.has_perm("formly.edit_survey", obj=field.survey):
        raise PermissionDenied()

    if request.method == "POST":
        if request.POST.get("action") == "field_update":
            form = FieldForm(data=request.POST, instance=field)
            field_choice_form = FieldChoiceForm(prefix="choices")
            if form.is_valid():
                form.save()
                return redirect(field)
    else:
        form = FieldForm(instance=field)
        field_choice_form = FieldChoiceForm(prefix="choices")
        likert_scale_form = LikertScaleForm()

    return render(request, "formly/design/survey_list.html", {
        "surveys": Survey.objects.all().order_by("-created"),
        "survey_form": SurveyCreateForm(user=request.user),
        "pages": field.page.survey.pages.all(),
        "selected_page": field.page,
        "selected_survey": field.survey,
        "fields": field.page.fields.all().order_by("ordinal"),
        "selected_field": field,
        "field_form": form,
        "field_choice_form": field_choice_form,
        "likert_scales": LikertScale.objects.all(),
        "likert_scale_form": likert_scale_form
    })


@require_POST
@login_required
def choice_delete(request, pk):
    choice = get_object_or_404(FieldChoice, pk=pk)
    if not request.user.has_perm("formly.edit_survey", obj=choice.field.survey):
        raise PermissionDenied()
    choice.delete()
    return JsonResponse({"html": ""})


@login_required
def choice_update(request, pk):
    choice = get_object_or_404(FieldChoice, pk=pk)

    if not request.user.has_perm("formly.edit_survey", obj=choice.field.survey):
        raise PermissionDenied()

    if request.method == "POST":
        form = FieldChoiceForm(
            data=request.POST,
            instance=choice
        )
        if form.is_valid():
            form.save()
            return redirect(choice.field.page)
    else:
        form = FieldChoiceForm(instance=choice)

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
