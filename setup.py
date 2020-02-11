#!/usr/bin/env python3
from setuptools import setup

setup(
    name="tap-abcfinancial",
    version="0.1.1",
    description="Singer.io tap for extracting data",
    author="Simon Data",
    url="http://simondata.com",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_abcfinancial"],
    install_requires=[
        "singer-python==5.2.0",
        'requests==2.18.4',
        "pendulum==1.2.0",
        "tap-kit@ https://pypicloud-production.simondata.net/simple/tap-kit/"
    ],
    dependency_links=[
        "https://pypicloud-production.simondata.net/simple/tap-kit/",
    ],
    entry_points="""
    [console_scripts]
    tap-abcfinancial=tap_abcfinancial:main
    """,
    packages=["tap_abcfinancial"],
    include_package_data=True,
)
