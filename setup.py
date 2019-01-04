from setuptools import setup

setup(
    name="pytest-docgen",
    packages=['pytest_docgen', 'sphinxext'],
    version="1.1.0",
    # the following makes a plugin available to pytest
    entry_points={
        'pytest11': [
            'pytest_docgen = pytest_docgen.pytest_docgen',
        ],
        'sphinx.builders': [
            'pytest_docgen = pytest_docgen.sphinxext.collapsible_block',
        ]
    },

    # custom PyPI classifier for pytest plugins
    classifiers=[
        "Framework :: Pytest",
    ],
    install_requires=['rstcloth', 'tabulate']
)
