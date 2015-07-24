import json
from django import forms


class MultipleTextField(forms.MultiValueField):
    def __init__(self, fields_length, **kwargs):
        fields = tuple(forms.CharField(max_length=200) for _ in range(fields_length))
        kwargs.update({"fields": fields})
        super(MultipleTextField, self).__init__(**kwargs)
        self.fields_length = fields_length

    def compress(self, data_list):
        return json.dumps(data_list)


class MultiTextWidget(forms.MultiWidget):
    def __init__(self, widgets_length, **kwargs):
        widgets = (forms.TextInput() for _ in range(widgets_length))
        kwargs.update({"widgets": widgets})
        super(MultiTextWidget, self).__init__(**kwargs)

    def decompress(self, value):
        return json.loads(value) if value is not None else []
