try:
    from django.urls import reverse  # noqa
except ImportError:
    # Django 1.8
    from django.core.urlresolvers import reverse  # noqa
