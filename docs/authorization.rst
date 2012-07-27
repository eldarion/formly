.. _authorization:


Authorization
=============

``formly`` ships with an auth backend that by default, when added to
your ``AUTHENTICATION_BACKENDS`` setting will segment the create,
edit, delete and results viewing based on the ``reauest.user`` being
the ``Survey.creator``.

You can override this by writing your own auth backend and using in
it's place.

The permission labels used are as follows:


formly.view_survey_list
-----------------------

Can the user see the list of published and unpublished surveys


formly.create_survey
--------------------

Can the user create a survey


formly.view_survey_detail
-------------------------

Can the user view the survey's detail. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.change_survey_name
-------------------------

Can the user change the survey's name. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.publish_survey
---------------------

Can the user publish the survey. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.duplicate_survey
-----------------------

Can the user duplicate the survey. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.edit_survey
------------------

Can the user edit the survey. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.view_results
-------------------

Can the user view the survey's results. The survey object in question is
passed to the ``has_perm`` method of the auth backend.


formly.delete_object
--------------------

Can the user delete the object in question. The object will be either a
``Survey``, ``Page``, ``Field``, or a ``FieldChoice``.

