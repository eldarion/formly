from django import template

from ..forms.widgets import LikertSelect, RatingSelect

register = template.Library()


@register.filter
def is_likert(field):
    return isinstance(field.field.widget, LikertSelect)


@register.filter
def is_rating(field):
    return isinstance(field.field.widget, RatingSelect)
