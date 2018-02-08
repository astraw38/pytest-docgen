from setuptools import setup

setup(
    name="pytest-docgen",
    packages=['pytest_docgen'],

    # the following makes a plugin available to pytest
    entry_points={
        'pytest11': [
            'pytest_docgen = pytest_docgen.pytest_docgen',
        ]
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
)
