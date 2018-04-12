
# Formly

[![](https://img.shields.io/pypi/v/formly.svg)](https://pypi.python.org/pypi/formly/)

[![CircleCi](https://img.shields.io/circleci/project/github/eldarion/formly.svg)](https://circleci.com/gh/eldarion/formly)
[![Codecov](https://img.shields.io/codecov/c/github/eldarion/formly.svg)](https://codecov.io/gh/eldarion/formly)
[![](https://img.shields.io/github/contributors/eldarion/formly.svg)](https://github.com/eldarion/formly/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/eldarion/formly.svg)](https://github.com/eldarion/formly/pulls)
[![](https://img.shields.io/github/issues-pr-closed/eldarion/formly.svg)](https://github.com/eldarion/formly/pulls?q=is%3Apr+is%3Aclosed)

[![](https://img.shields.io/badge/license-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


## Table of Contents

* [Overview](#overview)
  * [Supported Django and Python versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Optional Requirements](#optional-requirements)
  * [Usage](#usage)
  * [Fields](#fields)
  * [Templates](#templates)
  * [Authorization](#authorization)
  * [Callbacks](#callbacks)
* [Change Log](#change-log)
* [License](#license)


## formly

### Overview

``formly`` is a forms/survey generator for dynamically constructed multi-page surveys with the ability to be non-linear.

`formly` is an app that provides an out of the box solution to building adhoc
forms to collect data from end users. It is multi-faceted in that it provides
interfaces for building multi-page forms, interfaces for executing the survey,
as well as views for reviewing results.

Also, it is non-linear, meaning that you can route users taking the survey to
different pages based on what they answered on certain questions. This allows
you to create very rich surveys that dive deep on detail you care about while
not wasting the time of users who would otherwise have to go through questions
that do not apply to them.

Development sponsored by [Midwest Communications](http://mwcradio.com/) and [Massachusetts General Hospital](http://www.massgeneral.org/).


#### Supported Django and Python versions

Django \ Python | 2.7 | 3.4 | 3.5 | 3.6
--------------- | --- | --- | --- | ---
1.11 |  *  |  *  |  *  |  *  
2.0  |     |  *  |  *  |  *


## Documentation

### Installation

To install formly:

```shell
    $ pip install formly
```

Add `formly` to your ``INSTALLED_APPS`` setting:

```python
    INSTALLED_APPS = [
        # other apps
        "formly",
    ]
```

Next, add `formly.urls` to your project urlpatterns:

```python
    urlpatterns = [
        # other urls
        url(r"^surveys/", include("formly.urls", namespace="formly")),
    ]
```

Finally, if you want to use formly's permission authentications,
add `formly.auth_backend.AuthenticationBackend` to your settings
AUTHENTICATION_BACKENDS:

```python
    AUTHENTICATION_BACKENDS = [
        # other authentication backends
        "formly.auth_backend.AuthenticationBackend",
    ]
```

### Optional Requirements

In order to use built-in templates, add the following dependencies to your project:

* pinax-theme-bootstrap (not required if you use different block names)
* django-bootstrap-form (required for form rendering in templates)

```python
    INSTALLED_APPS = [
        # other apps
        "bootstrapform",
    ]
```


### Usage

`formly` is designed to be plug-and-play, in that after you install `formly`
using it should be as simple as creating and publishing surveys through
the web interface.

After installation, browse to wherever you mounted the urls for `formly` and
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


### Fields

`formly` enables you to create questions with a multitude of field types that
will control the dynamic rendering and processing of form input on each page of
your survey.

All field types tie directly to a specific `field` and `widget`
configuration as found in `django.forms`. The other attributes that can be
passed into every field, `label`, `help_text`, and `required` can be
set and managed at design time.

For the field types that accept choices, there is the ability to set key/value
pairs for each field that are used to populate the choices attribute for the
field to be used for both display as well as form validation upon execution.

#### Boolean (True/False)

Renders and processes input using `django.forms.BooleanField`.

#### Checkbox (Multiple Choice, Multiple Answers)

A field generated from a `django.forms.MultipleChoiceField` with a
`django.forms.CheckboxInput` widget, populated with choices specified
at design time. This field allows for multiple selections.

#### Date

Provides a way to constrain input to dates only. It is
generated from a `django.forms.DateField`.

#### Likert Scale

A `django.forms.ChoiceField` populated with choices specified at design time.
The field template `formly/templates/bootstrapform/field.html` emits:

```html
    <ul class="likert-question">
        {{ field }}
    </ul>
```

for hooking in CSS design. The following sample CSS presents a Likert field
in familiar horizontal layout. You should add this (or similar) CSS to your
project to get Likert-scale presentation.

```css
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
```

#### Media (File Upload)

Enables users to upload content as a response using `django.forms.FileField`.

#### Multiple Text (Multiple Free Responses - Single Lines)

Presents a number of single line fields.
The number of fields is specified at design time.

#### Radio (Multiple Choice, Pick One)

A `django.forms.ChoiceField` with a `django.forms.RadioSelect` widget,
populated with choices specified at design time.

#### Rating Scale

A `django.forms.ChoiceField` populated with choices specified at design time.
The field template `formly/templates/bootstrapform/field.html` emits:

```html
    <ul class="rating-question">
        {{ field }}
    </ul>
```

#### Select (Multiple Choice, Pick One - Dropdown)

A select field generated from a `django.forms.ChoiceField` with a
`django.forms.Select` widget, populated with choices specified at design time.

#### Text (Free Response, One Line)

A field for open ended text input and is interpreted as `django.forms.CharField`.

#### TextArea (Free Response, Box)

A `django.forms.CharField` with a `django.forms.Textarea` widget used
to collect longer form text input.


### Templates

`formly` ships with some stock templates that are based on
`pinax-theme-bootstrap` and `django-forms-bootstrap`. You are not required
to use these of course and in case you are rolling your own templates, here
is what the views in `formly` expect.

#### `formly/design/choice_form.html`

**Context:** `form`, `choice`, `page`

**Extends:** `formly/design/survey_edit_base.html`

Provides the ability to update the values for a particular choice for a choice field.

#### `formly/design/field_confirm_delete.html`

**Context:** `form`, `field`

**Extends:** `site_base.html`

Rendered to supply a delete confirmation form for field deletion.

#### `formly/design/field_form.html`

**Context:** `form`, `field`, `page`, `field_choice_form`

**Extends:** `formly/design/survey_edit_base.html`

Rendered for a user interface to update a field.

#### `formly/design/fieldchoice_confirm_delete.html`

**Context:** `form`, `fieldchoice`

**Extends:** `site_base.html`

Rendered to supply a delete confirmation form for field choice deletion.

#### `formly/design/page_confirm_delete.html`

**Context:** `form`, `page`

**Extends:** `site_base.html`

Rendered to supply a delete confirmation form for page deletion.

#### `formly/design/page_form.html`

**Context:** `form`, `page`, `field_form`

**Extends:** `formly/design/survey_edit_base.html`

Displays the user interface for updating a page object.

#### `formly/design/survey_confirm_delete.html`

**Context:** `form`, `survey`

**Extends:** `site_base.html`

Rendered to supply a delete confirmation form for survey deletion.

#### `formly/design/survey_detail.html`

**Context:** `survey`

**Extends:** `site_base.html`

Displays the detail for a survey.

#### `formly/design/survey_edit_base.html`

**Context:** `page`

**Extends:** `subnav_base.html`

**Extended By:** `formly/design/choice_form.html`, `formly/design/field_form.html`, `formly/design/page_form.html`

A base template to provide common sub-navigation.

#### `formly/design/survey_form.html`

**Context:** `form`

**Extends:** `site_base.html`

Contains the creation form for creating a new survey object.

#### `formly/design/survey_list.html`

**Context:** `unpublished_surveys`, `published_surveys`

**Extends:** `site_base.html`

This template receives all surveys in the system split between two context objects,
one for published surveys and the other for unpublished surveys.

#### `formly/results/home.html`

**Context:** `survey`

**Extends:** `site_base.html`

Displays the results of a given survey.

#### `formly/run/page.html`

**Context:** `form`, `page`

**Extends:** `site_base.html`

Rendered for the end user to complete a particular survey. Always
rendered with the appropriate page for the user.

#### `formly/results/remap.html`

**Context:** `field`, `unmapped_answers`, `answer_string`

**Extends:** `site_base.html`

Allows the end user to "remap" answers for a `MULTI_TEXT` field, e.g.

```
# User A's answers to the question,
# "What are your favorite Central City establishments?"

Big Belly Burger
Star Labs
Jitters

# Answers for User B

Big Belty Burger
STAR labs
Palmer Technologies
```

Passing `Big Belly Burger` as the `answer_string` URL argument would allow
the end user to map `Big Belty Burger` as an answer to `Big Belly Burger`.


#### `formly/bootstrapform/field.html`

**Context:** `field`

This modified `django-bootstrap-form` template renders the various field types,
including special handling for Likert and Rating fields.


### Authorization

`formly` ships with an auth backend that by default, when added to
your `AUTHENTICATION_BACKENDS` setting will segment the create,
edit, delete and results viewing based on `request.user` being
the `Survey.creator`.

You can override this by writing your own auth backend and using in
it's place.

The permission labels used are as follows:


#### `formly.view_survey_list`

User can see the list of published and unpublished surveys.

#### `formly.create_survey`

User can create a survey.

#### `formly.view_survey_detail`

User can view the survey's detail. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.change_survey_name`

User can change the survey's name. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.publish_survey`

User can publish the survey. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.duplicate_survey`

User can duplicate the survey. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.edit_survey`

User can edit the survey. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.view_results`

User can view the survey's results. The survey object in question is
passed to the `has_perm` method of the auth backend.

#### `formly.delete_object`

User can delete the object in question. The object will be either a
`Survey`, `Page`, `Field`, or a `FieldChoice`.


### Callbacks

Callbacks are a way to provide functionality to `formly` that requires some
runtime decision making instead of just a setting. They are callables
defined in settings.py and ship some sane defaults.


#### `FORMLY_COMPLETE_REDIRECT_CALLBACK`

**Default:** `formly.callbacks.survey_complete_redirect`

**Arguments:** `survey`

**Expected Return:** a url that will be passed to `redirect()`


## Change Log

### Unreleased
_TBD_

### 2.0.0
* Add the ability to remap `MULTIPLE_TEXT` answers
* Introduce `FORMLY_TEST_ARGS` pattern to run a restricted version of the test suite

**Backwards Incompatible Changes**
Previously, answers stored in `FieldResult.answer` for `Field`s with the `MULTIPLE_TEXT` field_type were getting serialized to JSON twice.

This release fixes this by:
- Removing extra serialization/de-serialization from the `compress` and `decompress` methods in the form field / widget
- Running a data migration that removes the double serialization for existing entries


### 1.0.0

* Add Django v1.11, 2.0 support
* Drop Django 1.8, 1.9, 1.10, and Python 3.3 support
* Add URL namespacing (i.e. urlname "formly_survey_results" is now "formly:survey_results") **Backwards Incompatible**
* Rename URL names, removing "dt_" and "rt_" prefixes **Backwards incompatible**
* Move documentation into README and standardize layout
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description
* Add migration checking to test suite

### 0.15.0

* fix bug where widget instances were passed instead of widget classes (#34)

### 0.14.0

* add hookset to support customizing available field type choices when designing a survey

### 0.13.0

* fix field mapping bug (#30)
* improve output of MultipleTextField widget (#20)

### 0.12.0

* fix broken migrations from 0.11.0

### 0.11.0

* add support for Rating field

### 0.10.2

* fix app to work with a custom user module
* add missing migration for formly.Field

### 0.10.1

* fix Field.form_field() bug when Likert field has no choices

### 0.10

* add Likert-style field widget and presentation


### 0.9

* make label and help_text textfields

### 0.6

* changed field label descriptions to be more suitable for less technical audiences
* made compatible with Django > 1.5
* drop unique constraint on field label

### 0.5

* made urls Django 1.5 compatible
* add maximum_choices field
* drop unique constraint on field label

### 0.4.2

* fixed multiple choice field
* added survey to context

### 0.4.1

* fixed serialization bug, note this is a backwards incompatible change
  if you have previously stored results

### 0.4

* added authorization checks for all the views

### 0.3

* added ability to control redirection at the end of a survey

### 0.2

* added ability to change the ordering of fields on a page

### 0.1

* initial release


## License

Copyright (c) 2012-2018 Patrick Altman and contributors under the [BSD license](https://opensource.org/licenses/BSD-3-Clause).
