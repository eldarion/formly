import json

from django.forms import TextInput
from django.forms.widgets import MultiWidget, RadioSelect
from django.template.loader import render_to_string


class MultiTextWidget(MultiWidget):
    def __init__(self, widgets_length, **kwargs):
        widgets = (TextInput() for _ in range(widgets_length))
        kwargs.update({"widgets": widgets})
        super(MultiTextWidget, self).__init__(**kwargs)

    def decompress(self, value):
        return json.loads(value) if value is not None else []

    def format_output(self, rendered_widgets):
        return render_to_string(
            "formly/run/_multiple_input.html",
            context={
                "inputs": rendered_widgets
            }
        )


class LikertSelect(RadioSelect):
    """
    This class differentiates Likert-scale radio selects
    from "normal" radio selects for presentation purposes.
    """
    pass


class RatingSelect(RadioSelect):
    pass
