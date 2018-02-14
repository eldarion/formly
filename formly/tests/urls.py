from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("formly.urls", namespace="formly")),
]
