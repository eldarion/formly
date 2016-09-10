from django.conf.urls import include


urlpatterns = [
    (r"^", include("formly.urls")),
]
