#!/usr/bin/env python
import setuptools


setuptools.setup(
    author='Bryan Stitt',
    author_email='bryan@stitthappens.com',
    description='Mark shows unwatched on a schedule.',
    long_description=__doc__,
    entry_points={
        'console_scripts': [
            'loot = loot:main',
        ],
    },
    install_requires=[
        'click',
        'PyYAML',
    ],  # keep this in sync with requirements.in
    name='loot',
    packages=setuptools.find_packages(),
    version='0.0.1.dev0',
)
