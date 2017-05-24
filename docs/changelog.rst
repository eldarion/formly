.. _changelog:

ChangeLog
=========

0.10.2
------

- fix app to work with a custom user module
- add missing migration for formly.Field

0.10.1
------

- fix Field.form_field() bug when Likert field has no choices

0.10
-----

- add Likert-style field widget and presentation


0.9
---

- make label and help_text textfields


0.6
---

- changed field label descriptions to be more suitable for less technical audiences
- made compatible with Django > 1.5
- drop unique constraint on field label


0.5
---

- made urls Django 1.5 compatible
- add maximum_choices field
- drop unique constraint on field label

0.4.2
-----

- fixed multiple choice field
- added survey to context

0.4.1
-----

- fixed serialization bug, note this is a backwards incompatible change
  if you have previously stored results

0.4
---

- added authorization checks for all the views


0.3
---

- added ability to control redirection at the end of a survey


0.2
---

- added ability to change the ordering of fields on a page


0.1
---

- initial release
