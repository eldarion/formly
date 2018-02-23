from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from formly.forms.design import (
    FieldChoiceForm,
    FieldForm,
    OrdinalScaleForm,
    PageUpdateForm,
    SurveyCreateForm,
)
from formly.models import Field, FieldChoice, OrdinalScale, Page, Survey
from formly.utils.views import BaseDeleteView

try:
    from account.decorators import login_required
except ImportError:
    from django.contrib.auth.decorators import login_required


@login_required
def survey_list(request):
    if not request.user.has_perm("formly.view_survey_list"):
        raise PermissionDenied()  # pragma: no cover -> never invoked because @login_required

    return render(
        request,
        "formly/design/survey_list.html",
        context={
            "surveys": Survey.objects.all().order_by("-created"),
            "survey_form": SurveyCreateForm(user=request.user)
        })


@login_required
def survey_detail(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.view_survey_detail", obj=survey):
        raise PermissionDenied()

    response = render(
        request,
        "formly/design/survey_list.html",
        context={
            "surveys": Survey.objects.all().order_by("-created"),
            "survey_form": SurveyCreateForm(user=request.user),
            "pages": survey.pages.all(),
            "selected_survey": survey
        })
    return response


@login_required
def page_detail(request, pk):
    page = get_object_or_404(Page, pk=pk)

    if not request.user.has_perm("formly.view_survey_detail", obj=page.survey):
        raise PermissionDenied()

    return render(
        request,
        "formly/design/survey_list.html",
        context={
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
        raise PermissionDenied()  # pragma: no cover -> never invoked because @login_required

    if request.method == "POST":
        form = SurveyCreateForm(request.POST, user=request.user)
        if form.is_valid():
            survey = form.save()
            return redirect(survey.first_page())
    else:
        form = SurveyCreateForm(user=request.user)

    return render(
        request,
        "formly/design/survey_form.html",
        context={
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
    return JsonResponse({
        "status": "OK",
        "name": survey.name
    })


@require_POST
@login_required
def survey_publish(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.publish_survey", obj=survey):
        raise PermissionDenied()

    survey.publish()
    return redirect("formly:survey_list")


@require_POST
@login_required
def survey_duplicate(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.duplicate_survey", obj=survey):
        raise PermissionDenied()

    duped = survey.duplicate()
    return redirect("formly:survey_detail", pk=duped.pk)


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
def field_create(request, pk):
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
    # @@@ break this apart into separate views
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
            field_form = FieldForm(data=request.POST, prefix="fields")
            if field_form.is_valid():
                field = field_form.save(commit=False)
                field.page = page
                field.survey = page.survey
                field.save()
                return redirect(page)
    else:
        form = PageUpdateForm(instance=page)
        field_form = FieldForm(prefix="fields")
    return render(
        request,
        "formly/design/page_form.html",
        context={
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
            context={
                "selected_page": field.page,
                "fields": field.page.fields.all().order_by("ordinal"),
                "selected_field": field
            },
            request=request
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
            context={
                "selected_page": field.page,
                "fields": field.page.fields.all().order_by("ordinal"),
                "selected_field": field
            },
            request=request
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
    return render(
        request,
        "formly/design/survey_list.html",
        context={
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
    scale = get_object_or_404(OrdinalScale, pk=scale_pk)
    field.scale = scale
    field.save()
    return JsonResponse({
        "html": render_to_string(
            "formly/design/_likert_scales.html",
            context={
                "selected_field": field,
                "likert_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_LIKERT)
            },
            request=request
        )
    })


@require_POST
@login_required
def likert_scale_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, field_type=Field.LIKERT_FIELD)
    likert_scale_form = OrdinalScaleForm(request.POST, balanced=True)
    if likert_scale_form.is_valid():
        scale = likert_scale_form.save(commit=False)
        scale.kind = OrdinalScale.ORDINAL_KIND_LIKERT
        scale.save()
        choices = likert_scale_form.cleaned_data["scale"]
        max_score = int((len(choices) - 1) / 2)
        min_score = -max_score
        for index, score in enumerate(range(min_score, max_score + 1)):
            scale.choices.create(
                label=choices[index],
                score=score
            )
        field.scale = scale
        field.save()
        likert_scale_form = OrdinalScaleForm()
    return JsonResponse({
        "html": render_to_string(
            "formly/design/_likert_scale_form.html",
            context={
                "selected_field": field,
                "likert_scale_form": likert_scale_form,
            },
            request=request
        ),
        "fragments": {
            ".likert-scales": render_to_string(
                "formly/design/_likert_scales.html",
                context={
                    "selected_field": field,
                    "likert_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_LIKERT),
                },
                request=request
            )
        }
    })


@require_POST
@login_required
def rating_scale_set(request, field_pk, scale_pk):
    field = get_object_or_404(Field, pk=field_pk, field_type=Field.RATING_FIELD)
    scale = get_object_or_404(OrdinalScale, pk=scale_pk)
    field.scale = scale
    field.save()
    return JsonResponse({
        "html": render_to_string(
            "formly/design/_rating_scales.html",
            context={
                "selected_field": field,
                "rating_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_RATING)
            },
            request=request
        )
    })


@require_POST
@login_required
def rating_scale_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, field_type=Field.RATING_FIELD)
    rating_scale_form = OrdinalScaleForm(request.POST)
    if rating_scale_form.is_valid():
        scale = rating_scale_form.save(commit=False)
        scale.kind = OrdinalScale.ORDINAL_KIND_RATING
        scale.save()
        choices = rating_scale_form.cleaned_data["scale"]
        for index, choice in enumerate(choices):
            scale.choices.create(
                label=choice,
                score=index
            )
        field.scale = scale
        field.save()
        rating_scale_form = OrdinalScaleForm()
    return JsonResponse({
        "html": render_to_string(
            "formly/design/_rating_scale_form.html",
            context={
                "selected_field": field,
                "rating_scale_form": rating_scale_form
            },
            request=request
        ),
        "fragments": {
            ".rating-scales": render_to_string(
                "formly/design/_rating_scales.html",
                context={
                    "selected_field": field,
                    "rating_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_RATING)
                },
                request=request
            )
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
            likert_scale_form = OrdinalScaleForm()
            rating_scale_form = OrdinalScaleForm()
    else:
        form = FieldForm(instance=field)
        field_choice_form = FieldChoiceForm(prefix="choices")
        likert_scale_form = OrdinalScaleForm()
        rating_scale_form = OrdinalScaleForm()

    return render(
        request,
        "formly/design/survey_list.html",
        context={
            "surveys": Survey.objects.all().order_by("-created"),
            "survey_form": SurveyCreateForm(user=request.user),
            "pages": field.page.survey.pages.all(),
            "selected_page": field.page,
            "selected_survey": field.survey,
            "fields": field.page.fields.all().order_by("ordinal"),
            "selected_field": field,
            "field_form": form,
            "field_choice_form": field_choice_form,
            "likert_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_LIKERT),
            "likert_scale_form": likert_scale_form,
            "rating_scales": OrdinalScale.objects.filter(kind=OrdinalScale.ORDINAL_KIND_RATING),
            "rating_scale_form": rating_scale_form
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

    return render(
        request,
        "formly/design/choice_form.html",
        context={
            "form": form,
            "choice": choice,
            "page": choice.field.page
        })


class SurveyDelete(BaseDeleteView):
    model = Survey
    success_url_name = "formly:survey_list"


class PageDelete(BaseDeleteView):
    model = Page
    success_url_name = "formly:survey_detail"
    pk_obj_name = "survey"


class FieldDelete(BaseDeleteView):
    model = Field
    success_url_name = "formly:page_update"
    pk_obj_name = "page"


class ChoiceDelete(BaseDeleteView):
    model = FieldChoice
    success_url_name = "formly:field_update"
    pk_obj_name = "field"
