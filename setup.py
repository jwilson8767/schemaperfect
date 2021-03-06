#!/usr/bin/env python
"""
Run `./setup.py test` to execute tests or `python -m pytest schemaperfect --doctest-modules`
Run `./setup.py build` to build
Dev install via `pip install -e .`
"""


import os
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# Version info
MAJOR = 0
MINOR = 5
MICRO = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: BSD License",
               "Operating System :: OS Independent",
               "Programming Language :: Python :: 3.6",
               "Programming Language :: Python :: 3.7",
               "Topic :: Scientific/Engineering"]

# Description should be a one-liner:
DESCRIPTION = "schemaperfect: generate Python APIs from JSONSchema specifications"

# Long description will go up on the pypi page
LONG_DESCRIPTION = """
JSONSchema API Generator
========================
The schemaperfect_ package provides tools for auto-generation of Python
APIs from JSONSchema_ specifications.

See more information in the README_.

.. _README: https://github.com/jwilson8767/schemaperfect/blob/master/README.md
.. _JSONSchema: http://json-schema.org/
.. _schemaperfect: https://github.com/jwilson8767/schemaperfect
"""

###############################################################################
# The following versioning code is adapted from the scipy package (BSD license)
# http://github.com/scipy/scipy
# (C) 2003-2017 SciPy Developers

def git_version():
    """Return the git revision as a string"""
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError:
        GIT_REVISION = "Unknown"

    return GIT_REVISION

def get_version_info():
    """
    Adding the git rev number needs to be done inside
    write_version_py(), otherwise the import of version messes
    up the build under Python 3.
    """
    FULLVERSION = VERSION
    if os.path.exists('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists('schemaperfect/version.py'):
        # must be a source distribution, use existing version file
        # load it as a separate module to not load schemaperfect/__init__.py
        import imp
        version = imp.load_source('schemaperfect.version',
                                  'schemaperfect/version.py')
        GIT_REVISION = version.git_revision
    else:
        GIT_REVISION = "Unknown"

    if not ISRELEASED:
        FULLVERSION += '.dev0+' + GIT_REVISION[:7]

    return FULLVERSION, GIT_REVISION


def write_version_py(filename='schemaperfect/version.py'):
    cnt = '''
# This file is automatically generated by the setup.py script
long_description = """{long_description}"""
short_version = '{version}'
version = '{version}'
full_version = '{full_version}'
git_revision = '{git_revision}'
release = {isrelease}
if not release:
    version = full_version
'''
    FULLVERSION, GIT_REVISION = get_version_info()
    with open(filename, 'w') as f:
        f.write(cnt.format(long_description=LONG_DESCRIPTION,
                           version=VERSION,
                           full_version=FULLVERSION,
                           git_revision=GIT_REVISION,
                           isrelease=str(ISRELEASED)))

# End of code adapted from SciPy
###############################################################################

def setup_package():
    write_version_py()

    metadata = dict(
        name="schemaperfect",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        maintainer="Joshua Wilson",
        maintainer_email="jwilson8767@gmail.com",
        url="http://github.com/jwilson8767/schemaperfect",
        include_package_data=True,
        license="BSD",
        author="Joshua Wilson",
        author_email="jwilson8767@gmail.com",
        platforms="OS Independent",
        package_data={},
        install_requires=["jsonschema"],
        python_requires='>3.6',
        tests_require=["pytest"],
        cmdclass={
            'test': PyTest,
        },
    )

    metadata['version'] = get_version_info()[0]
    metadata['packages'] = find_packages()

    setup(**metadata)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['schemaperfect', '--doctest-modules']
        self.test_suite = True

    def run_tests(self):

        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


if __name__ == '__main__':
    setup_package()
