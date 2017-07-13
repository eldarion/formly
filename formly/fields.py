from django import forms


class LimitedMultipleChoiceField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.maximum_choices = kwargs.pop("maximum_choices", None)
        super(LimitedMultipleChoiceField, self).__init__(*args, **kwargs)
    # @@@ validate using maximum_choices
