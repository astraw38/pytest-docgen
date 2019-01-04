import glob
from os.path import splitext, basename
from setuptools import setup, find_packages

setup(
    name="pytest-docgen",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    py_modules=[splitext(basename(i))[0] for i in glob.glob('src/pytest_docgen/sphinxext/*.py')],
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
