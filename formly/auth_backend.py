from django.contrib.auth.backends import ModelBackend


class AuthenticationBackend(ModelBackend):
    """
    Permissions that do not receive an object:

      * formly.view_survey_list
      * formly.create_survey

    Permissions that receive a survey object:

      * formly.view_survey_detail
      * formly.change_survey_name
      * formly.publish_survey
      * formly.duplicate_survey
      * formly.edit_survey
      * formly.view_results

    Permissions that receive different object types:

      * formly.delete_object
    """
    supports_object_permissions = True
    supports_anonymous_user = True

    def has_perm(self, user, perm, obj=None):
        permissions = [
            "formly.view_survey_list",
            "formly.create_survey",
        ]
        survey_permissions = [
            "formly.view_survey_detail",
            "formly.change_survey_name",
            "formly.publish_survey",
            "formly.duplicate_survey",
            "formly.edit_survey",
            "formly.view_results"
        ]
        if perm in permissions:
            return user.is_authenticated()
        if perm in survey_permissions:
            return obj and user == obj.creator
        if perm == "formly.delete_object":
            if obj is None:
                return False
            if hasattr(obj, "creator"):
                return user == obj.creator
            if hasattr(obj, "survey"):
                return user == obj.survey.creator
            if hasattr(obj, "page"):
                return user == obj.page.survey.creator
            if hasattr(obj, "field"):
                return user == obj.field.page.survey.creator
            return False
        return super(AuthenticationBackend, self).has_perm(user, perm)
