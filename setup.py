from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import codecs
import os

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()

setup(
    name='PyVDF',
    version='1.0.4',
    tests_require=['pytest'],
    packages=['PyVDF'],
    url='https://github.com/amreuland/PyVDF',
    author='Austin Reuland',
    author_email='amreuland@gmail.com',
    keywords = "VDF KeyValues Valve",
    description='Python Library for reading VDFs and Valve KeyValue files',
    platforms='any',
    cmdclass={'test': PyTest},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities'
    ]
)