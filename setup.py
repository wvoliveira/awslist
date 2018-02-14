from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from awslist import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        error = call(['py.test', '--cov=awslist', '--cov-report=term-missing'])
        raise SystemExit(error)


setup(
    name='awslist',
    version=__version__,
    description='Bootstrap AWS EC2 list',
    long_description=long_description,
    url='https://github.com/wvoliveira/awslist',
    author='Wellington Oliveira',
    author_email='oliveira@live.it',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: MIT',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='cli aws ec2',
    packages=find_packages('.', exclude=['docs', 'tests*']),
    package_data={'awslist': ['data/css/*.css', 'data/js/*.js']},
    install_requires=['boto3', 'colorama'],
    extras_require={'test': ['coverage', 'pytest', 'pytest-cov']},
    entry_points={'console_scripts': ['awslist=awslist.cli:main']},
    cmdclass={'test': RunTests},
)
