#!/usr/bin/env python
import poco_lite
import sys
import platform
from setuptools import setup, find_packages

requires = ['pyaml==16.12.2', 'docopt==0.6.2', 'docker-compose>=1.11.2']

if platform.system() == "Darwin" and sys.version_info[0] == 3:
    requires.append("certifi>=2017.4.17")
    requires.append("Scrapy >= 1.4.0")

setup_options = dict(
    name='poco-lite',
    version=poco_lite.__version__,
    description='poco lets you catalogue and manage your Docker projects using simple YAML files to shorten the route '
                'from finding your project to initialising it in your environment.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Shiwaforce.com',
    url='https://www.shiwaforce.com',
    packages=find_packages(),
    package_data={'': ['poco.yml',
                       'docker-compose.yml',
                       'command-hierarchy.yml'
                       ]},
    include_package_data=True,
    install_requires=requires,
    entry_points={
      'console_scripts': ['poco=poco_lite.poco:main'],
    },
    license="Apache License 2.0",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)

print(sys.argv)
setup(**setup_options)
