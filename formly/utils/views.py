from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import DeleteView


class BaseDeleteView(LoginRequiredMixin, DeleteView):
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
