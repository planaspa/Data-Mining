import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class pytest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        sys.exit(os.system('py.test tests'))

setup(
    name='Beer Tweeting',
    version='1.0',
    author='Pablo Lanaspa',
    author_email='planaspa@gmail.com',
    description='Description........',
    license='MIT',
    url='https://github.com/planaspa/Data-Mining',
    keywords='beer twitter',
    py_modules=['src'],
    test_suite="tests", 
    install_requires=[
        'numpy>=1.8.2',
        'six>=1.5.2',
        'pytz>=2014.9',
        'tornado>=3.1.1',
        'pyparsing>=2.0.3',
        'matplotlib>=1.4.2',
        'networkx>=1.9.1',
        'docopt>=0.6.0,<0.7.0',
    ],
    dependency_links = [
        "https://github.com/matplotlib/basemap" #BaseMap
    ],
    packages=find_packages('src'),
    long_description=open('README.md').read(),
    cmdclass={'test': pytest},
    tests_require=['pytest'],
    scripts=['src/'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
)
