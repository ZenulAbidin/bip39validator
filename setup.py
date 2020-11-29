from setuptools import setup, find_packages
import os.path

with open(os.path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open(os.path.join('.', 'bip39validator', '__version__.py')) as g:
    exec(g.read(), version)

setup(
    name='bip39validator',
    version=version['__version__'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    package_dir={'bip39validator': 'bip39validator'},
    url='https://github.com/ZenulAbidin/bip39validator',
    license='MIT',
    author='Ali Sherief',
    author_email='alihsherief@linuxmail.org',
    description='Validator for BIP39 wordlists',
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
    ],
    project_urls={
        'Changelog': 'https://github.com/ZenulAbidin/bip39validator/blob/master/CHANGELOG.md',
        'Issue Tracker': 'https://github.com/ZenulAbidin/bip39validator/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Jellyfish 0.7.1 drops Python 3.4. No good reason to pin this version
        # in particular, but some of the other versions have lots of bugs.
        # rich 4.2.1 fixes a fatal error in progress.track
        # requests 2.20.1 fixes a security vulnerability
        # None of the pinned releases have bugs that affect operation of BIP39
        # Validator
        'jellyfish', 'rich', 'requests', 'validation'
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'bip39validator = bip39validator.__main__:main',
        ]
    },
)
