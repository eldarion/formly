class FormlyDefaultHookset(object):

    @property
    def field_type_choices(self):
        """
        Customize available field type choices when designing a survey
        default: Field.FIELD_TYPE_CHOICES
        """
        from formly.models import Field
        return Field.FIELD_TYPE_CHOICES


class HookProxy(object):

    def __getattr__(self, attr):
        from formly.conf import settings
        return getattr(settings.FORMLY_HOOKSET, attr)


hookset = HookProxy()
