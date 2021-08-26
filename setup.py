# coding: utf-8

import os
from setuptools import setup
from setuptools import find_packages


README_FPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')

setup(
    name="sorl-watermark",
    version="1.2.0",
    url="https://github.com/originell/sorl-watermark",
    author="Luis Nell",
    author_email="luis@originell.org",
    packages=find_packages(),
    platforms="any",
    description="Image based watermarks for sorl-thumbnail",
    long_description=open(README_FPATH).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics",
    ],
    install_requires=["sorl-thumbnail"],
)
