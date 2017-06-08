from django import forms

from formly.models import Survey, Page, Field, FieldChoice, OrdinalScale


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


class OrdinalScaleForm(forms.ModelForm):

    scale = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.balanced = kwargs.pop("balanced", False)
        super(OrdinalScaleForm, self).__init__(*args, **kwargs)

    def clean_scale(self):
        scale = self.cleaned_data["scale"]
        if not scale:
            raise forms.ValidationError("You must provide scale values, delimited by commas.")
        scale_choices = [s.strip() for s in scale.split(",")]
        if self.balanced and len(scale_choices) % 2 != 1:
            raise forms.ValidationError("A Likert scale must have an odd number of choices.")
        return scale_choices

    class Meta:
        model = OrdinalScale
        fields = [
            "name",
            "scale"
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
