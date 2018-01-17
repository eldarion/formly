from urllib import unquote

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from formly.models import Survey, Field
from formly.utils.remapping import create_answer_list


@login_required
def survey_results(request, pk):
    survey = get_object_or_404(Survey, pk=pk)

    if not request.user.has_perm("formly.view_results", obj=survey):
        raise PermissionDenied()

    return render(request, "formly/results/home.html", {
        "survey": survey,
    })


class RemapView(LoginRequiredMixin, DetailView):
    model = Field
    context_object_name = "question"
    template_name = "formly/results/remap.html"

    def get_context_data(self, **kwargs):
        context = super(RemapView, self).get_context_data(**kwargs)

        field_results = self.object.results.all()
        context["unmapped_results"] = sorted(create_answer_list(field_results))
        context["remap_answer"] = unquote(self.kwargs.get("answer_string"))
        return context

    def post(self, request, *args, **kwargs):
        remapped_answers = request.POST.getlist("mapping")
        answer_string = self.kwargs.get("answer_string")
        question = self.get_object()
        mapping = dict([(unquote(remapped_answer), answer_string) for remapped_answer in remapped_answers])

        for mapped_answer in question.mapping.keys():
            answer = question.mapping[mapped_answer]
            if answer in answer_string:
                del question.mapping[mapped_answer]

        question.mapping.update(mapping)
        question.save()
        for result in question.results.all().select_related("question"):
            result.save()

        if request.is_ajax():
            return JsonResponse(question.mapping)
        return HttpResponseRedirect(reverse("formly_survey_results", args=[question.survey.pk]))
