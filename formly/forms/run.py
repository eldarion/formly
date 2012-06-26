from django import forms

from formly.models import SurveyResult, FieldResult


class PageForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop("page")
        super(PageForm, self).__init__(*args, **kwargs)
        
        for field in self.page.fields.all():
            self.fields[field.name] = field.form_field()
    
    def save(self, user):
        result, _ = SurveyResult.objects.get_or_create(
            survey=self.page.survey,
            user=user
        )
        for field in self.page.fields.all():
            field_result, _ = FieldResult.objects.get_or_create(
                survey=self.page.survey,
                page=self.page,
                result=result,
                question=field
            )
            field_result.answer = self.cleaned_data[field.name]
            field_result.save()
