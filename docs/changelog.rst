.. _changelog:

ChangeLog
=========

0.9.1
-----

- add `fieldtype` to PageForm field widget.attrs


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
