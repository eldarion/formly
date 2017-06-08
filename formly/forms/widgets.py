from django.forms.widgets import RadioSelect


class LikertSelect(RadioSelect):
    """
    This class differentiates Likert-scale radio selects
    from "normal" radio selects for presentation purposes.
    """
    pass


class RatingSelect(RadioSelect):
    pass
