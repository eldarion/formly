import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LimitedMultipleChoiceField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.maximum_choices = kwargs.pop("maximum_choices")

        self.default_error_messages.update({
            "maximum_choices": _("You may select at most %(maximum)d choices (%(selected)d selected)")
        })

        super(LimitedMultipleChoiceField, self).__init__(*args, **kwargs)

    def validate(self, value):
        super(LimitedMultipleChoiceField, self).validate(value)

        selected_count = len(value)
        if self.maximum_choices and selected_count > self.maximum_choices:
            raise ValidationError(
                self.error_messages["maximum_choices"],
                code="maximum_choices",
                params={"maximum": self.maximum_choices, "selected": selected_count},
            )


class MultipleTextField(forms.MultiValueField):
    def __init__(self, fields_length, **kwargs):
        fields = tuple(forms.CharField(max_length=200) for _ in range(fields_length))
        kwargs.update({"fields": fields})
        super(MultipleTextField, self).__init__(**kwargs)
        self.fields_length = fields_length

    def compress(self, data_list):
        return json.dumps(data_list)
