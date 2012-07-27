.. _callbacks:


Callbacks
=========

Callbacks are a way to provide functionality to formly that requires some
runtime decision making instead of just a setting. They are callables
that are defined in settings and ship some sane defaults.


``FORMLY_COMPLETE_REDIRECT_CALLBACK``
-------------------------------------

:Default: ``formly.callbacks.survey_complete_redirect``
:Arguments: ``survey``
:Expected Return: a url that will be passed to ``redirect()``
