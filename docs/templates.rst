.. _templates:

Templates
=========

``formly`` ships with some stock templates that are based on
``pinax-theme-bootstrap`` and ``django-forms-bootstrap``. You are not required
to use these of course and in case you are rolling your own templates, here
is what the views in ``formly`` expect.


``formly/design/choice_form.html``
----------------------------------

:Context: ``form``, ``choice``, ``page``
:Extends: ``formly/design/survey_edit_base.html``

This is the template that provides the ability to update the values for a
particular choice for a choice field.


``formly/design/field_confirm_delete.html``
-------------------------------------------

:Context: ``form``, ``field``
:Extends: ``site_base.html``

This is the template is rendered to supply a delete confirmation form for
field deletion.


``formly/design/field_form.html``
----------------------------------

:Context: ``form``, ``field``, ``page``, ``field_choice_form``
:Extends: ``formly/design/survey_edit_base.html``

This is the template is rendered for a user interface to update a field.


``formly/design/fieldchoice_confirm_delete.html``
-------------------------------------------------

:Context: ``form``, ``fieldchoice``
:Extends: ``site_base.html``

This is the template is rendered to supply a delete confirmation form for
field choice deletion.


``formly/design/page_confirm_delete.html``
------------------------------------------

:Context: ``form``, ``page``
:Extends: ``site_base.html``

This is the template is rendered to supply a delete confirmation form for
page deletion.


``formly/design/page_form.html``
--------------------------------

:Context: ``form``, ``page``, ``field_form``
:Extends: ``formly/design/survey_edit_base.html``

This is the template is that displays the user interface for updating a
page object.


``formly/design/survey_confirm_delete.html``
--------------------------------------------

:Context: ``form``, ``survey``
:Extends: ``site_base.html``

This is the template is rendered to supply a delete confirmation form for
survey deletion.


``formly/design/survey_detail.html``
------------------------------------

:Context: ``survey``
:Extends: ``site_base.html``

This template displays the detail for a survey.


``formly/design/survey_edit_base.html``
---------------------------------------

:Context: ``page``
:Extends: ``subnav_base.html``
:Extended By: ``formly/design/choice_form.html``, ``formly/design/field_form.html``, ``formly/design/page_form.html``

This a base template to provide some common subnav.


``formly/design/survey_form.html``
----------------------------------

:Context: ``form``
:Extends: ``site_base.html``

This template hosts the creation form for creating a new survey object.


``formly/design/survey_list.html``
----------------------------------

:Context: ``unpublished_surveys``, ``published_surveys``
:Extends: ``site_base.html``

This template receives all surveys in the system split between two context objects,
one for published surveys and the other for unpublished surveys.


``formly/results/home.html``
----------------------------

:Context: ``survey``
:Extends: ``site_base.html``

A template for displaying the results of a given survey.


``formly/run/page.html``
------------------------

:Context: ``form``, ``page``
:Extends: ``site_base.html``

This template is rendered for the end user to complete a particular survey, it is always
rendered with the appropriate page for the user.


``formly/bootstrapform/field.html``
------------------------

:Context: ``field``

This modified ``django-bootstrap-form`` template renders the various field types,
including special handling for Likert and Rating fields.
