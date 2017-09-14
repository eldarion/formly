import json
from urllib import unquote

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from formly.models import Survey, Field


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
    context_object_name = 'question'
    template_name = "formly/results/remap.html"

    def create_answer_list(self, fieldresults):

        answer_list = []

        for result in fieldresults:
            if type(result.answer['answer']) is not dict:
                answers = json.loads(result.answer['answer'])
            else:
                answers = result.answer['answer']

            if type(answers) is unicode:
                answer_list.append(answers.strip().upper())
            else:
                for answer in answers:
                    answer_list.append(answer.strip().upper())

        # Quickly remove duplicates
        return list(set(answer_list))

    def get_context_data(self, **kwargs):
        context = super(RemapView, self).get_context_data(**kwargs)

        field_results = self.object.results.unmapped()
        context['unmapped_results'] = sorted(self.create_answer_list(field_results))
        context['remap_answer'] = unquote(self.kwargs.get('answer_string'))
        return context

    def post(self, request, *args, **kwargs):
        remapped_answers = request.POST.getlist('mapping')
        question = self.get_object()
        mapping = dict([(unquote(remapped_answer), self.kwargs.get('answer_string')) for remapped_answer in remapped_answers])
        question.mapping.update(mapping)
        question.save()
        for result in question.results.all():
            result.save()

        return HttpResponseRedirect(reverse('formly_survey_results', args=[question.survey.pk]))
