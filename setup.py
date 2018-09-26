from setuptools import setup

setup(
    name="pytest-docgen",
    packages=['pytest_docgen'],
    version="1.0.2",
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
    install_requires=['rstcloth', 'tabulate']
)
