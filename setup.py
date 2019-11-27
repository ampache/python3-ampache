"""
Setup file for srlearn
Refer to https://github.com/lachlan-00/python3-ampache
"""

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension
from codecs import open
from os import path

# Get __version__ from _meta.py
with open(path.join("src", "_meta.py")) as f:
    exec(f.read())

setup(
    name="ampache",
	py_modules=["ampache"],
    package_dir={'': 'src'},
    author="Lachlan de Waard (lachlan-00)",
    author_email="lachlan.00@gmail.com",
    version=__version__,
    description="Python library for Amapche XML-API",
    long_description="This library is able to connect to Ampache and return the xml or binary data received from the queries.",
    include_package_data=False,
    url="https://github.com/lachlan-00/python3-ampache",
    download_url="https://github.com/lachlan-00/python3-ampache",
    license="GPL-3.0",
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: PHP Classes",
    ],
    keywords="",
    install_requires=[""],
)