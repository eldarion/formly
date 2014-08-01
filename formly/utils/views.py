from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView

from django.contrib.auth.decorators import login_required


def cbv_decorator(decorator):
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls
    return _decorator


@cbv_decorator(login_required)
class BaseDeleteView(DeleteView):
    success_url_name = ""
    pk_obj_name = ""

    def get_object(self, queryset=None):
        obj = super(BaseDeleteView, self).get_object(queryset=queryset)

        if not self.request.user.has_perm("formly.delete_object", obj=obj):
            raise PermissionDenied()

        return obj

    def get_template_names(self):
        names = super(BaseDeleteView, self).get_template_names()
        return [
            name.replace("formly/", "formly/design/")
            for name in names
        ]

    def get_success_url(self):
        kwargs = {}
        if self.pk_obj_name:
            kwargs["pk"] = getattr(self.object, self.pk_obj_name).pk
        return reverse(self.success_url_name, kwargs=kwargs)
