from setuptools import setup, find_packages

setup(
    name="pytest-docgen",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    version="1.3.0",
    description="An RST Documentation Generator for pytest-based test suites",
    maintainer="Ashley Straw",
    maintainer_email="as.fireflash38@gmail.com",
    author="Ashley Straw",
    author_email="as.fireflash38@gmail.com",
    keywords=["pytest", "sphinx", "rst", "testing"],
    url="https://github.com/astraw38/pytest-docgen",
    download_url="https://github.com/astraw38/pytest-docgen/tarball/v1.3.0/",
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["pytest_docgen = pytest_docgen.pytest_docgen",],},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest",],
    install_requires=["rstcloth", "tabulate"],
)
