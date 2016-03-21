import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys
import uuid

from benzo import __version__ as version_string


requirements_path = os.path.join(
    os.path.dirname(__file__),
    'requirements.txt',
)
try:
    from pip.req import parse_requirements
    requirements = [
        str(req.req) for req in parse_requirements(
            requirements_path,
            session=uuid.uuid1()
        )
    ]
except ImportError:
    requirements = []
    with open(requirements_path, 'r') as in_:
        requirements = [
            req for req in in_.readlines()
            if not req.startswith('-')
            and not req.startswith('#')
        ]


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


setup(
    name='benzo',
    version=version_string,
    url='https://github.com/coddingtonbear/benzo',
    description=(
        'Hand-curate your artisanal REST requests more easily.'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requirements,
    tests_require=['tox', ],
    cmdclass = {'test': Tox},
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'benzo = benzo.cmdline:main'
        ],
    },
)
