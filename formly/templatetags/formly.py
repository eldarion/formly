from django import template

from ..forms.widgets import LikertSelect

register = template.Library()


@register.filter
def is_likert(field):
    return isinstance(field.field.widget, LikertSelect)
