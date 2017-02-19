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
``django.forms.RadioSelect`` widget, populated with choices specified at
design time.


dropdown field
--------------

The ``dropdown field`` is a select field generated from a
``django.forms.ChoiceField`` with a ``django.forms.Select`` widget, populated
with choices specified at design time.


checkbox field
--------------

The ``checkbox field`` is a field generated from a
``django.forms.MultipleChoiceField`` with a ``django.forms.CheckboxInput`` widget,
populated with choices specified at design time. This field allows for
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


multiple text field
-------------------

The ``multiple text`` field type presents a number of single line fields.
The number of fields is specified at design time.


likert scale field
------------------

The ``likert scale`` field type is a ``django.forms.ChoiceField``,
populated with choices specified at design time.
Presentation uses formly/templates/bootstrapform/field.html and sets
``<ul class="likert-question">`` for CSS design. Here is sample CSS
which presents a Likert field in familiar horizontal layout:

    form .likert-question {
      list-style:none;
      width:100%;
      margin:0;
      padding:0 0 35px;
      display:block;
      border-bottom:2px solid #efefef;
    }
    form .likert-question:last-of-type {
      border-bottom:0;
    }
    form .likert-question:before {
      content: '';
      position:relative;
      top:13px;
      left:13%;
      display:block;
      background-color:#dfdfdf;
      height:4px;
      width:75%;
    }
    form .likert-question li {
      display:inline-block;
      width:19%;
      text-align:center;
      vertical-align: top;
    }
    form .likert-question li input[type=radio] {
      display:block;
      position:relative;
      top:0;
      left:50%;
      margin-left:-6px;
    }
    form .likert-question li label {
      width:100%;
    }
