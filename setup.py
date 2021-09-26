from codecs import open
from os import path

from setuptools import find_packages, setup

__version__ = "2.0.0"

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="sorl-watermark",
    version=__version__,
    description="Adds support for watermarks to sorl-thumbnail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/originell/sorl-watermark",
    download_url="https://github.com/originell/sorl-watermark/tarball/" + __version__,
    project_urls={
        "Source": "https://github.com/originell/sorl-watermark",
        "Release notes": "https://github.com/originell/sorl-watermark/releases",
        "Changelog": "https://github.com/originell/sorl-watermark/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/originell/sorl-watermark/issues",
    },
    license="MIT",
    keywords="django sorl thumbnail watermark",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Graphics",
    ],
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    author="Luis Nell",
    author_email="luis@originell.org",
    install_requires=["sorl-thumbnail>=12.5.0"],
)
