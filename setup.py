from setuptools import setup
from setuptools import find_packages

setup(
    name='sorl-watermark',
    version='0.0.1',
    url='https://github.com/originell/sorl-watermark',
    author='Luis Nell',
    author_email='cooperate@originell.org',
    packages=find_packages(),
    platform='any',
    description='Image based watermarks for sorl-thumbnail',
    long_description=open('README.md').read(),
    classifiers=[
        "Development Status :: 1 - Planning"
        "Environment :: Web Environment"
        "Framework :: Django"
        "Intended Audience :: Developers"
        "License :: OSI Approved :: BSD License"
        "Operating System :: OS Independent"
        "Programming Language :: Python"
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
        "Topic :: Multimedia :: Graphics"
    ],
    install_requires=[
        'sorl-thumbnail',
    ],
)
