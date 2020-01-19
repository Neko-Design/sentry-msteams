#!/usr/bin/env python
"""
sentry-msteams
==============

An extension for `Sentry <https://getsentry.com>`_ which posts notifications
to `Microsoft Teams <https://products.office.com/en-us/microsoft-teams/group-chat-software>`_.

:license: APACHE2, see LICENSE for more details.
"""

from setuptools import setup, find_packages
import os

cwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
readme_text = open(os.path.join(cwd, 'README.md')).read()

setup(
    name='sentry-msteams',
    version='0.7.0',
    author='Ewen McCahon',
    author_email='hi@ewenmccahon.me',
    url='https://github.com/Neko-Design/sentry-msteams',
    long_description=readme_text,
    long_description_content_type="text/markdown",
    license='apache2',
    description='A Sentry extension which posts notifications to Microsoft Teams (https://products.office.com/en-us/microsoft-teams/group-chat-software).',
    packages=find_packages(),
    install_requires=[
        'sentry',
    ],
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'msteams = msteams',
        ],
        'sentry.plugins': [
            'msteams = msteams.plugin:TeamsPlugin',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)