from django import forms

from formly.models import SurveyResult, FieldResult


class PageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop("page")
        super(PageForm, self).__init__(*args, **kwargs)
        
        for field in self.page.fields.all():
            self.fields[field.name] = field.form_field()
    
    def save(self, user):
        survey_result, _ = SurveyResult.objects.get_or_create(
            survey=self.page.survey,
            user=user
        )
        
        for field in self.page.fields.all():
            if field.field_type == field.MEDIA_FIELD:
                defaults = {"answer": {"answer": ""}, "upload": self.cleaned_data[field.name]}
            else:
                defaults = {"answer": {"answer": self.cleaned_data[field.name]}, "upload": ""}
            
            # @@@ Can't do a get_or_create as JSONField doesn't seem to respect defaults
            qs = FieldResult.objects.filter(
                survey = self.page.survey,
                page = self.page,
                result = survey_result,
                question = field
            )
            
            if qs.exists():
                result = qs.get()
                result.answer = defaults["answer"]
                result.upload = defaults["upload"]
                result.save()
            else:
                result = FieldResult.objects.create(
                    survey = self.page.survey,
                    page = self.page,
                    result = survey_result,
                    question = field,
                    answer = defaults["answer"],
                    upload = defaults["upload"]
                )