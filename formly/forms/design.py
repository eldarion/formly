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
    
    target = forms.ModelChoiceField(
        label="Next Page",
        queryset=Page.objects.all(),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super(PageUpdateForm, self).__init__(*args, **kwargs)
        self.fields["target"].queryset = self.instance.survey.pages.exclude(
            pk=self.instance.pk
        )
    
    class Meta:
        model = Page
        fields = [
            "subtitle",
            "target"
        ]


class FieldForm(forms.ModelForm):
    
    class Meta:
        model = Field
        fields = [
            "label",
            "field_type",
            "help_text",
            "required"
        ]


class FieldChoiceForm(forms.ModelForm):
    
    target = forms.ModelChoiceField(
        label="Next Page",
        queryset=Page.objects.all(),
        required=False
    )
    
    def __init__(self, field, *args, **kwargs):
        super(FieldChoiceForm, self).__init__(*args, **kwargs)
        self.field = field
        self.fields["target"].queryset = self.field.survey.pages.exclude(
            pk=self.field.page.pk
        )
    
    class Meta:
        model = FieldChoice
        fields = [
            "label",
            "target"
        ]
