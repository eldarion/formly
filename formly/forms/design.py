from django import forms

from formly.models import Survey, Page, Field, FieldChoice


class SurveyCreateForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = [
            "name",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(SurveyCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(SurveyCreateForm, self).save(commit=False)
        instance.creator = self.user
        if commit:
            instance.save()
        return instance


class PageUpdateForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = [
            "subtitle"
        ]


class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = [
            "label",
            "field_type",
            "help_text",
            "maximum_choices",
            "required",
            "expected_answers",
        ]


class FieldChoiceForm(forms.ModelForm):

    class Meta:
        model = FieldChoice
        fields = [
            "label"
        ]
