#!/usr/bin/env python
"""
sentry-msteams
==============

An extension for `Sentry <https://getsentry.com>`_ which posts notifications
to `Microsoft Teams <https://products.office.com/en-us/microsoft-teams/group-chat-software>`_.

:license: APACHE2, see LICENSE for more details.
"""

from setuptools import setup, find_packages

setup(
    name='sentry-msteams',
    version='0.1.0',
    author='Ewen McCahon',
    author_email='ewen.m.mccahon@student.uts.edu.au',
    url='https://github.com/Neko-Design/sentry-msteams',
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