# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='django-model-urls',
    version='0.4.0',
    description='DRY way to manage url parameters associated with a model instance based on Jingo.',
    long_description=open('README.md').read(),
    author='Vincent Agnano',
    author_email='vincent.agnano@scopyleft.fr',
    url='http://github.com/vinyll/django-model-urls',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ]
)
