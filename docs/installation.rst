.. _installation:

Installation
============

* Requirements:
 * django-jsonfield==0.9.13

* Optional Requirements (to use the built in templates):
 * pinax-theme-bootstrap (not required if you use different block names)
 * django-forms-bootstrap (required for form rendering in templates)

* To install::

    pip install formly

* Add ``'formly'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        # other apps
        "formly",
    )

* Mount the ``formly.urls`` somewhere::

    urlpatterns = patterns("",
        ...
        url(r"^surveys/", include("formly.urls")),
        ...
    )
