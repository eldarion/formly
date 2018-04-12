#!/usr/bin/env python
import os
import sys

import django

from django.conf import settings


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


PACKAGE_ROOT=os.path.abspath(os.path.dirname(__file__))
DEBUG = True

DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",

        "bootstrapform",
        "formly",
        "formly.tests",
        "pinax.templates",
    ],
    AUTHENTICATION_BACKENDS=[
        "formly.auth_backend.AuthenticationBackend"
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                os.path.join(PACKAGE_ROOT, "templates"),
            ],
            "APP_DIRS": True,
            "OPTIONS": {
                "debug": DEBUG,
                "context_processors": [
                    "django.contrib.auth.context_processors.auth",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.i18n",
                    "django.template.context_processors.media",
                    "django.template.context_processors.static",
                    "django.template.context_processors.tz",
                    "django.template.context_processors.request",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ],
    SITE_ID=1,
    ROOT_URLCONF="formly.tests.urls",
    SECRET_KEY="notasecret",

    # Use a speedy password hasher!
    PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher",
    ],
    # Disable migrations
    MIGRATION_MODULES = DisableMigrations()
)


def runtests(*test_args):
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = os.environ.get("FORMLY_TEST_ARGS", "formly.tests").split(" ")
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ["tests"]

    failures = runner_class(verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests(*sys.argv[1:])
