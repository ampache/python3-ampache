"""
Setup file
Refer to https://github.com/ampache/python3-ampache
"""

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension
from codecs import open
from os import path

# Get __version__ from _meta.py
with open(path.join("src", "_meta.py")) as f:
    exec(f.read())

_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="ampache",
	py_modules=["ampache"],
    package_dir={'': 'src'},
    author="Lachlan de Waard (lachlan-00)",
    author_email="lachlan.00@gmail.com",
    version=__version__,
    description="Python library for Amapche XML & JSON API",
    long_description=LONG_DESCRIPTION,
    include_package_data=False,
    url="https://github.com/ampache/python3-ampache",
    download_url="https://github.com/ampache/python3-ampache",
    license="GPL-3.0",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: PHP Classes",
        "Intended Audience :: Developers",
    ],
    keywords="",
    install_requires=[""],
)