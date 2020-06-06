#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'requests>=2.23.0', 'beautifulsoup4>=4.9.1']

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Allen Shaw",
    author_email='lonsty@sina.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Search emoji by keywords in terminal.",
    entry_points={
        'console_scripts': [
            'emoji=emoji.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='emoji',
    name='emoji2',
    packages=find_packages(include=['emoji', 'emoji.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lonsty/emoji',
    version='0.2.0',
    zip_safe=False,
)
