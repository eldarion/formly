from django import forms

from formly.models import SurveyResult, Field, FieldResult


class FieldResultMixin(object):
    
    def save_result(self, field, user):
        if not hasattr(self, "_survey_result"):
            self._survey_result, _ = SurveyResult.objects.get_or_create(
                survey=field.survey,
                user=user
            )
        
        if field.field_type == Field.MEDIA_FIELD:
            defaults = {"answer": {"answer": ""}, "upload": self.cleaned_data[field.name]}
        else:
            defaults = {"answer": {"answer": self.cleaned_data[field.name]}, "upload": ""}
        
        qs = FieldResult.objects.filter(
            survey=field.survey,
            page=None,
            result=self._survey_result,
            question=field
        )
        if qs.exists():
            result = qs.get()
            result.answer = defaults["answer"]
            result.upload = defaults["upload"]
            result.save()
        else:
            result = FieldResult.objects.create(
                survey=field.survey,
                page=None,
                result=self._survey_result,
                question=field,
                answer=defaults["answer"],
                upload=defaults["upload"]
            )
        return result


class PageForm(FieldResultMixin, forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop("page")
        super(PageForm, self).__init__(*args, **kwargs)
        for field in self.page.fields.all():
            self.fields[field.name] = field.form_field()
    
    def save(self, user):
        for field in self.page.fields.all():
            self.save_result(field, user)


class TargetForm(FieldResultMixin, forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop("choice").target
        super(TargetForm, self).__init__(*args, **kwargs)
        self.fields[self.target.name] = self.target.form_field()
    
    def save(self, user):
        return self.save_result(self.target, user)
