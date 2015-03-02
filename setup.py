
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "curc-bench",
    version = "0.0.0",
    author = "Research Computing",
    author_email = "",
    description = ("HPC Benchmarking"),
    license = "BSD",
    keywords = "",
    url = "",
    packages=['src/bench'],
    install_requires=['NumPy>=1.7.0','pandas>=0.7.3'],
    tests_require=['nose'],
    # test_suite="src/tests",
    long_description=read('README'),
    classifiers=[
        "License :: BSD License",
    ],
)