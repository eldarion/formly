.. _usage:

Usage
=====

``formly`` is designed to be pretty plug-and-play, in that after you install
it, using it should be as simple as creating and publishing surveys through
the web interface.

After installation, browse to whereever you mounted the urls for `formly` and
you'll see an interface to be able to create a new survey. From here you can
create a survey and begin editing pages. Pages in `formly` represent each
step of the survey. The user will be guided through each page of the survey
in the appropriate order saving each page at a time.

For each page, you can give a title and add as many fields as you desire. If
the field is a type that requires choices, then you will have the option
on the fields detail/edit form to add choices. An optional value that can
be supplied for a choice answer is the page to redirect the user to if they
select that answer.

If you have multiple choice fields in a single page with conflicting page
routing, `formly` resolves to the first page it encounters. For example, if
you had a question that had choice B route to page 3 and another question
later in the form that had choice C route to page 5 and the user answered
both questions with choice B and choice C, the user would go to page 3
next. Keep this in mind when building surveys.
