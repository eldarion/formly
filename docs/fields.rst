.. _fields:

Fields
======

``formly`` enables you to create questions with a multitude of field types that
will control the dynamic rendering and processing of form input on each page of
your survey.

All field types tie directly to a specific ``field`` and ``widget``
configuration as found in ``django.forms``. The other attributes that can be
passed into every field, ``label``, ``help_text``, and ``required`` can be
set and managed at design time.

For the field types that accept choices, there is the ability to set key/value
pairs for each field that are used to populate the choices attribute for the
field to be used for both display as well as form validation upon execution.


text field
----------

The ``text field`` is a field for open ended text input and is interpreted as
``django.forms.CharField``.


textarea
--------

The ``textarea`` field type is a ``django.forms.CharField`` with a
``django.forms.Textarea`` widget to be used to collect longer form text input.


radio choices
-------------

The ``radio choices`` field type is a ``django.forms.ChoiceField`` with a
``django.forms.RadioSelect`` widget, populated with choices as specified at
design time.


dropdown field
--------------

The ``dropdown field`` is a select field generated from a
``django.forms.ChoiceField`` with a ``django.forms.Select`` widget, populated
with choices as specified at design time.


checkbox field
--------------

The ``checkbox field`` is a field generated from a
``django.forms.MultipleChoiceField`` with a ``django.forms.CheckboxInput`` widget,
populated with choices as specified at design time. This field allows for
multiple selections.


date field
----------

The ``date field`` provides a way to constrain input to dates only. It is
generated from a ``django.forms.DateField``.


media upload field
------------------

The ``media upload field`` enables users to upload content as a response. It
is uses ``django.forms.FileField``.


boolean field
-------------

The ``boolean field`` renders and processes input using
``django.forms.BooleanField``.

