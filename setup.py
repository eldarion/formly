import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()

setup(
    author="Patrick Altman",
    author_email="paltman@eldarion.com",
    description="a dynamic form generator",
    name="formly",
    long_description=read("README.rst"),
    version="0.9",
    url="https://github.com/eldarion/formly",
    license="BSD",
    packages=find_packages(),
    package_data={
        "formly": []
    },
    test_suite="runtests.runtests",
    tests_require=[],
    install_requires=[
        "jsonfield>=1.0.3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
