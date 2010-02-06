from setuptools import setup

setup(
    name = "Supay",
    version = "0.0.3",
    description = "A simple Daemonizing module for Python scripts.",
    long_description = """\
An effective way to daemonize a Python script with some added
functionality like spawning new child processes and verify the status
of a running process.
This version includes a testing directory in the source file.
""",
    keywords = 'python, daemon, daemonize',
    license = 'GPLv3',
    include_package_data=True,
    author = "Alfredo Deza",
    author_email = "alfredodeza at gmail dot com",
    url = 'http://code.google.com/p/supay',
    py_modules = ['supay',],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]
    )

