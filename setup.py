import glob
from os.path import splitext, basename
from setuptools import setup

setup(
    name="pytest-docgen",
    packages=['pytest_docgen'],
    py_modules=[splitext(basename(i))[0] for i in glob.glob('pytest_docgen/sphinxext')],
    version="1.1.0",
    # the following makes a plugin available to pytest
    entry_points={
        'pytest11': [
            'pytest_docgen = pytest_docgen.pytest_docgen',
        ],
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
    install_requires=['rstcloth', 'tabulate']
)
