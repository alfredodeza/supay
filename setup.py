import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name = "Supay",
    version = "0.0.4",
    packages = find_packages(),
    scripts = ['supay.py'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt'],
        },

    # metadata for upload to PyPI
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "A daemonizing library for Python.",
    long_description = """\
 An effective way to daemonize a Python script with some added
 functionality like spawning a new child process and status verification
 """,

    license = "MIT",
    py_modules = ['supay',],
    keywords = "daemon daemonize start stop status spawn process processses",
    url = "http://code.google.com/p/supay",   

)

